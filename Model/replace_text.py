import os

def replace_text_in_file(file_path, old_text, new_text):
    with open(file_path, 'r', encoding='utf-8') as file:
        file_data = file.read()
    
    if old_text in file_data:
        new_data = file_data.replace(old_text, new_text)
        
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(new_data)
        
        print(f"Text replaced in: {file_path}")
    else:
        print(f"No text to replace in: {file_path}")

def replace_text_in_directory(directory_path, old_text, new_text):
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                replace_text_in_file(file_path, old_text, new_text)

if __name__ == "__main__":
    directory_path = input("Enter the directory path: ")
    old_text = input("Enter the text to be replaced: ")
    new_text = input("Enter the new text: ")
    
    replace_text_in_directory(directory_path, old_text, new_text)
    print("Text replacement completed.")
