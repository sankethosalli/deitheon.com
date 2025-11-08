#!/bin/bash

# Git push script for frontend

echo "🎨 Frontend - Git Push Script"
echo "=============================="
echo ""

# Check if there are changes
if [[ -z $(git status -s) ]]; then
    echo "✅ No changes to commit"
    exit 0
fi

# Show status
echo "📊 Current status:"
git status -s
echo ""

# Ask for commit message
read -p "💬 Enter commit message (or press Enter for default): " commit_msg

# Use default message if empty
if [ -z "$commit_msg" ]; then
    commit_msg="chore(frontend): update frontend code"
fi

# Add all changes
echo ""
echo "📦 Adding changes..."
git add .

# Commit
echo "💾 Committing..."
git commit -m "$commit_msg"

# Push
echo "🚀 Pushing to origin..."
git push

echo ""
echo "✅ Done! Frontend changes pushed successfully!"