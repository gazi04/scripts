# 🤖 tmux-sessions

## Overview

`tmux-sessions` is a simple shell script designed to streamline the creation of multiple isolated **Tmux** sessions using a single command. Instead of manually running `tmux new-session -s name` multiple times, you can pass all desired session names as arguments at once.

This tool is perfect for setting up your complete development environment (e.g., frontend, backend, database, monitoring) instantly.

## 🚀 Key Features

- **Batch Creation:** Create N new, detached Tmux sessions with one command.
- **Safety Check:** Automatically skips creating sessions if a session with the given name already exists.
- **Detached:** All sessions are created in the background, ready for you to attach to them.

## 💻 Setup Instructions

To use `tmux-sessions` from any directory, you must place the script in your system's `$PATH`. `/usr/local/bin` is the standard location for user-installed executables.

### Prerequisites

1. **Tmux** must be installed on your system.

### Installation Steps

1. **Save the Script:** Ensure the script content is saved in a file named `tmux-sessions.sh` (or just `tmux-sessions`) in a temporary location.
    
    > **Note:** For cleaner usage, it is recommended to use the name `tmux-sessions` (without the `.sh` extension) when placing it in `/usr/local/bin`.
    
2. **Make it Executable:** Grant execution permissions to the script.
    
    ```
    chmod +x tmux-sessions.sh
    ```
    
3. **Copy to PATH:** Copy the executable file to a directory included in your system's `$PATH`, such as `/usr/local/bin`. This step requires `sudo` privileges.
    
    ```
    # Assuming you are renaming it to remove the .sh extension for easier typing
    sudo cp tmux-sessions.sh /usr/local/bin/tmux-sessions
    ```
    
4. **Verification:** Confirm the script is in your path and has correct permissions.
    
    ```
    ls -l /usr/local/bin/tmux-sessions
    # Expected output should show executable permissions (e.g., -rwxr-xr-x)
    ```
    

## 💡 Usage

Run the script followed by the names of the sessions you want to create, separated by spaces.

### Syntax

```
tmux-sessions <session-name-1> <session-name-2> [session-name-n]...
```

### Example

To create sessions for a **Vim/NeoVim editor**, a **Git workflow**, and a **running server**:

```
tmux-sessions nvim git server
```

### Output

The script will confirm which sessions were created:

```
--- Starting Tmux Session Creation ---
✅ Created new session: nvim
✅ Created new session: git
✅ Created new session: server
--- Creation Complete ---
You can now list your sessions with: tmux ls
To attach to a session, use: tmux attach-session -t <session_name>
```

### Attaching to Sessions

Use the standard Tmux command to attach to any of the new sessions:

```
tmux attach-session -t nvim
```
