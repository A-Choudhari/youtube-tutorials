# Install Dependencies
# pip install django
# pip install opencv-python
# pip install pyaudio


from django.shortcuts import render
from django.http import StreamingHttpResponse, HttpResponse
import threading
from .camera import VideoCamera
import cv2
import pyaudio


def index(request):
    return render(request, "network/index.html")


# Webcam capture function
def webcam_stream(camera):
    while True:
        frame = camera.get_frame()  # Read a frame from the camera

        yield b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n'  # Yield the frame as a multipart response
        if cv2.waitKey(0) & 0xFF == ord(' '):
            break
    cv2.destroyAllWindows()  # Release the camera when done


def live_capture_view(request):
    try:
        return StreamingHttpResponse(webcam_stream(VideoCamera()), content_type="multipart/x-mixed-replace; boundary=frame")
    except Exception as e:
        print("Stream closed:", e)


def live_capture_audio(request):
    # Constants for audio capture
    CHUNK_SIZE = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    total_frames = int(RATE / CHUNK_SIZE * 5)
    # Create an instance of PyAudio
    audio = pyaudio.PyAudio()

    # Open a stream for audio capture
    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK_SIZE)

    # Open a stream for audio playback
    output_stream = audio.open(format=FORMAT,
                               channels=CHANNELS,
                               rate=RATE,
                               output=True)

    print("Recording and playback started. Press Ctrl+C to stop.")
    while True:
        data = stream.read(CHUNK_SIZE)
        output_stream.write(data)
        if cv2.waitKey(0) & 0xFF == ord(' '):
            break

    print("Recording and playback stopped.")

    # Close the audio streams
    stream.stop_stream()
    stream.close()
    output_stream.stop_stream()
    output_stream.close()

    # Terminate PyAudio
    audio.terminate()
    return HttpResponse("Finished code")