import re
import json
data_path = "./KakaoTalkChats.txt"

with open(data_path, 'r') as file:
    lines = file.readlines()

# Remove the pattern from each line
date_pattern = r'\d{4}년 \d{1,2}월 \d{1,2}일 오전 \d{1,2}:\d{1,2}, |\d{4}년 \d{1,2}월 \d{1,2}일 오후 \d{1,2}:\d{1,2}, '
result_lines = [re.sub(date_pattern, '', line) for line in lines]


def process_line(current_speaker, line, history):
    """Processes a line of chat, updating the history."""
    speaker_tag = f'{current_speaker} : '
    if line.startswith(speaker_tag):
        return history + line[len(speaker_tag):].strip() + ' '
    return history

def update_history(speakers, current_speaker, history, history_lines):
    """Updates the chat history when the speaker changes."""
    if history:
        history_lines.append(f'{current_speaker}: {history}')
    return '', speakers[1 - speakers.index(current_speaker)]
# Define speakers
counterpart_a = '종현'  # Placeholder for the actual name
counterpart_b = '이승주'

speaking = None
history_lines = []
history = ''
speakers = [counterpart_a, counterpart_b]

for line in result_lines:
    if speaking not in speakers:
        if line.startswith(counterpart_a):
            speaking = counterpart_a
        elif line.startswith(counterpart_b):
            speaking = counterpart_b
    else:
        if line.startswith(speakers[1 - speakers.index(speaking)]):
            history, speaking = update_history(speakers, speaking, history, history_lines)
        history = process_line(speaking, line, history)
# Handle the last history if any
if history:
    history_lines.append(f'{speaking}: {history}')
conversations = []
conversation = {"messages": [{"role": "system", "content": "종현 is a 20s Korean male who is having a chit-chat with a friend."}]}
current_role = "system"
current_message = ""

for line in history_lines:
    # Check if the line matches the date and time pattern
    if "종현:" in line:
        current_role = "assistant"
    elif "이승주:" in line:
        current_role = "user"
    # Split the line at the first colon and take everything after it as the message
    _, current_message = line.split(":", 1)
# Add the last message to the conversation
    conversation["messages"].append({"role": current_role, "content": current_message})
    if current_role == "assistant":
        conversations.append(conversation)
        conversation = {"messages": [{"role": "system", "content": "종현 is a 20s Korean male who is having a chit-chat with a friend."}]}
# Print the conversation in JSON format

output_file_path = "./KakaoTalkChats_conversations.json"

with open(output_file_path, 'w', encoding='utf-8') as file:
    for line in conversations:
        file.write('%s\n' % json.dumps(line, ensure_ascii=False))

print(f"Conversation saved to {output_file_path}")

# # Write to file
# with open("./KakaoTalkChats_modified.txt", 'w', encoding='utf-8') as file:
#     for line in history_lines:
#         file.write('%s\n' % json.dumps(line, ensure_ascii=False))