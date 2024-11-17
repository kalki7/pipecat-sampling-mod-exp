import base64
import uuid
import json

from pydantic import BaseModel

from pipecat.audio.utils import ulaw_to_pcm, pcm_to_ulaw
from pipecat.frames.frames import AudioRawFrame, Frame, StartInterruptionFrame
from pipecat.serializers.base_serializer import FrameSerializer


class CustomMediaSerializer(FrameSerializer):
    class InputParams(BaseModel):
        keeko_sample_rate: int = 8000
        sample_rate: int = 8000

    def __init__(self, params: InputParams = InputParams()):
        self._ucid = str(uuid.uuid4())
        self._params = params

    def serialize(self, frame: Frame) -> str | bytes | None:
        if isinstance(frame, AudioRawFrame):
            data = frame.audio
            
            serialized_data = pcm_to_ulaw(data, frame.sample_rate, self._params.keeko_sample_rate)
            payload = list(serialized_data)
            answer = {
                "type": "media",
                "ucid": self._ucid,
                "data": {
                    "samples": payload,
                    "bitsPerSample": 8,  # u-law data has 8 bits per sample
                    "sampleRate": self._params.keeko_sample_rate,
                    "channelCount": 1,  # Assuming mono audio
                    "numberOfFrames": len(payload),
                    "type": "data",
                },
            }
            print(answer)
            return json.dumps(answer)

        if isinstance(frame, StartInterruptionFrame):
            answer = {"type": "clear", "ucid": self._ucid}
            return json.dumps(answer)

    def deserialize(self, data: str | bytes) -> Frame | None:
        message = json.loads(data)

        if message["type"] != "media":
            return None
        else:
            payload = message["data"]["samples"]
            payload_bytes = bytes(payload)

            deserialized_data = ulaw_to_pcm(
                payload_bytes, self._params.twilio_sample_rate, self._params.sample_rate
            )
            audio_frame = AudioRawFrame(
                audio=deserialized_data, num_channels=message["data"]["channelCount"], sample_rate=self._params.sample_rate
            )
            print(audio_frame)
            return audio_frame
