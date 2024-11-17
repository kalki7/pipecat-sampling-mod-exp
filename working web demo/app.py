from fastapi import FastAPI, WebSocket
from functools import partial

import asyncio
import os
import sys

from pipecat.audio.vad.silero import SileroVADAnalyzer
from pipecat.frames.frames import LLMMessagesFrame, AudioRawFrame
from pipecat.pipeline.pipeline import Pipeline
from pipecat.pipeline.runner import PipelineRunner
from pipecat.serializers.protobuf import ProtobufFrameSerializer
from pipecat.pipeline.task import PipelineParams, PipelineTask
from pipecat.processors.aggregators.openai_llm_context import OpenAILLMContext
from pipecat.services.cartesia import CartesiaTTSService
from pipecat.services.deepgram import DeepgramSTTService
from pipecat.services.azure import AzureLLMService
from pipecat.transports.network.fastapi_websocket import (
    FastAPIWebsocketTransport,
    FastAPIWebsocketParams
)

from loguru import logger

from dotenv import load_dotenv

load_dotenv(override=True)

logger.remove(0)
logger.add(sys.stderr, level="DEBUG")

app = FastAPI()




@app.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    transport = FastAPIWebsocketTransport(
        params=FastAPIWebsocketParams(
            audio_out_sample_rate=8000,
            audio_out_bitrate=128000,
            audio_out_enabled=True,
            add_wav_header=True,
            vad_enabled=True,
            vad_analyzer=SileroVADAnalyzer(),
            vad_audio_passthrough=True,
            serializer = ProtobufFrameSerializer()
        ),
        websocket=websocket
    )
    async def _patched_receive_messages(self):
            async for message in self._websocket.iter_bytes():
                frame = self._params.serializer.deserialize(message)
                if not frame:
                    continue
                if isinstance(frame, AudioRawFrame):
                    await self.push_audio_frame(frame)
                else: 
                    await self._internal_push_frame(frame)
            await self._callbacks.on_client_disconnected(self._websocket)

    transport._input._receive_messages = partial(_patched_receive_messages, transport._input)

    llm = AzureLLMService(
            api_key=os.getenv("AZURE_CHATGPT_API_KEY"),
            endpoint=os.getenv("AZURE_CHATGPT_ENDPOINT"),
            model=os.getenv("AZURE_CHATGPT_MODEL"),
            api_version=os.getenv("AZURE_API_VERSION")
        )

    stt = DeepgramSTTService(api_key=os.getenv("DEEPGRAM_API_KEY"))

    tts = CartesiaTTSService(
        api_key=os.getenv("CARTESIA_API_KEY"),
        voice_id="41f3c367-e0a8-4a85-89e0-c27bae9c9b6d",
        sample_rate=8000,
    )

    messages = [
        {
            "role": "system",
            "content": """Your name is Party Registration Assistant. You're an intelligent registration assistant for a techno rave in San Francisco. Start by asking for my full name and contact details, then inquire about my interest in attending and any specific requests. As the conversation progresses, be mindful of any inconsistencies (e.g., if I initially say I'm attending and later mention I'm unsure). Gently address these conflicts, asking for clarification to ensure you're capturing the right information. Keep the conversation light, fun, and friendly while ensuring that everything makes sense based on my prior responses.
            Your responses will be converted to audio. Please do not include any special characters in your response other than '!' or '?'.""",
        },
    ]

    context = OpenAILLMContext(messages)
    context_aggregator = llm.create_context_aggregator(context)

    pipeline = Pipeline(
        [
            transport.input(),  # Websocket input from client
            stt,  # Speech-To-Text
            context_aggregator.user(),
            llm,  # LLM
            tts,  # Text-To-Speech
            transport.output(),  # Websocket output to client
            context_aggregator.assistant(),
        ]
    )

    task = PipelineTask(pipeline, params=PipelineParams(allow_interruptions=True))

    messages.append({"role": "system", "content": "Please introduce yourself to the user."})
    await task.queue_frames([LLMMessagesFrame(messages)])

    runner = PipelineRunner()

    while True:
        await runner.run(task)