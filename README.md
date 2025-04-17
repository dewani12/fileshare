# FileShare
# Overview 

> This project allows a **sender** to send files to **multiple receivers simultaneously** over a network using **WebSockets**.

## 🛠️ Technologies & Libraries Used

- **Python 3**
- **PyQt5** – for GUI
- **WebSocket**
- **`os`** – file handling
- **`threading`** – for parallel file transfer when needed
- **`socket`** – networking essentials
- **`asyncio`** – for concurrent operations without blocking

# 📸 Screenshots  
![Image](https://github.com/user-attachments/assets/221c9881-3a26-47ce-b151-2331adac7d63)  
![Image](https://github.com/user-attachments/assets/b8b27bae-bccb-4e67-b6f1-a5b8c5401016)

# ✅ Prerequisites  
Before running the project, make sure you have the following installed on your machine:

1. **Python 3.8+:** Download and install it from [python.org](https://www.python.org/downloads/).
   
2. **Pip:** Comes bundled with Python. You can verify by running:
   ```
   pip --version
   ```
3. **PyQt5:** Install it using pip.
   ```
   pip install PyQt5
   ```

# 💻 Local Setup 
```
git clone https://github.com/dewani12/fileshare.git
cd fileshare
python main.py
```

## 🚀 How to Use

## 📨 Sending a File

1. **Select the File**
   - Use the **File Selection** section of the UI to choose the file you want to send.

2. **Add Receiver(s)**
   - In the **Receiver Configuration** section of the UI, enter the **IP address** and **port** of the receiver.
   - Click to add the receiver.
   - Repeat the step to add multiple receivers.

3. **Review Receivers**
   - The list of added receivers will appear in the **Receivers Section**.
   - You can see the **connection status** and a **timeline bar** indicating transfer progress.

4. **Send the File**
   - Click the **"Send File"** button to start transferring the file to all added receivers simultaneously.

## 📥 Receiving a File

1. **Stop the Server** (if already running)
   - Ensure that no old instance of the server is running before restarting.

2. **Start the Receiver Server**
   - Choose a **port** (e.g., 8000, 9000, etc.).
   - Start the WebSocket server on that port.

3. **Check the Status Bar**
   - The receiver UI will update with server status (e.g., "Listening for incoming file...").

4. **Receive the File**
   - Once the file transfer begins, a progress bar and status update will be shown.
   - After completion, an **alert** will confirm that the file was received.
   - The file will be automatically downloaded into the **`Downloads/`** folder.

# Folder Structure (for easy navigation)
```
fileshare/
├── core/
│   ├── __init__.py
│   ├── reciever.py
│   └── sender.py
│
├── Downloads/
│
|── ui/
|   ├── __init__.py
|   ├── button.py
|   ├── reciever_widget.py
|   ├── sender_widget.py
├── main.py
```
