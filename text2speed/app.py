from gtts import gTTS
import os


def text_to_speech(text, language='vi', filename='output.mp3'):
    tts = gTTS(text=text, lang=language, slow=True)
    tts.save(filename)
    os.system(f"start {filename}")  # Mở tệp âm thanh sau khi tạo


# Ví dụ:
text = """
Winston Churchill từng nói rằng viết một cuốn sách phải trải qua năm giai đoạn, ở giai đoạn đầu tiên, nó chỉ là một thứ đồ chơi trong tay bạn. Nhưng đến giai đoạn cuối cùng, nó trở thành một tên bạo chúa muốn điều khiển cả cuộc đời bạn. Ngay khi bạn sắp sửa quy ngã và đầu hàng, bạn bỗng vùng lên giết chết tên bạo chúa và đưa cuốn sách của bạn đến với công luận. Đúng là như vậy! Nếu không có những con người tuyệt vời giúp đỡ chúng tôi trong việc hoàn thành cuốn sách này, tên bạo chúa kia đã có thể giành chiến thắng."
"""
text_to_speech(text, language='vi', filename='output.mp3')
