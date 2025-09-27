#!/bin/bash

if [ "$#" -eq 0 ]; then
    echo "Usage: $0 <session_name_1> <session_name_2> [session_name_n]..."
    echo "Example: $0 dev frontend backend monitor"
    exit 1
fi

echo "--- Starting Tmux Session Creation ---"

for SESSION_NAME in "$@"; do
    if ! tmux has-session -t "$SESSION_NAME" 2>/dev/null; then
        # Create a new detached session (-d) with the specified name (-s)
        tmux new-session -d -s "$SESSION_NAME"
        
        # You can optionally add a basic window/pane setup here.
        # Example: Split the window into two panes
        # tmux split-window -h -t "$SESSION_NAME"

        echo "✅ Created new session: $SESSION_NAME"
    else
        echo "⚠️ Session '$SESSION_NAME' already exists. Skipping."
    fi
done

echo "--- Creation Complete ---"
echo "You can now list your sessions with: tmux ls"
echo "To attach to a session, use: tmux attach-session -t <session_name>"

# Optional: Attach to the first session created
# tmux attach-session -t "$1"
