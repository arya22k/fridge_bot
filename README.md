# Fridge Bot

Fridge Bot is a Telegram-based system designed to reduce food waste in communal dormitories by notifying users when new food items are added and reminding them before items expire.

## Motivation
Food waste is a common issue in shared dorm refrigerators due to lack of visibility and communication. Fridge Bot aims to improve coordination among users by providing automated notifications and reminders.

## Features
- Telegram bot interface for shared fridge users
- Notifications when new items are added
- Scheduled reminders for items nearing expiration
- Centralized tracking of food items and expiry dates

## Tech Stack
- Python
- Telegram Bot API
- Database (specify: SQLite / MongoDB / etc.)

## How It Works
1. Users register with the fridge bot via Telegram
2. When a user adds an item, it is stored in the database with an expiry date
3. The bot sends notifications to all connected users
4. Periodic background jobs check for expiring items and send alerts

## Future Improvements
- Data analytics on food usage patterns
- Machine learning to predict expiration risk
- Improved privacy controls for shared environments

## Contributors
- Udhaya Bhuvanesh
- Arya
- Audrey 
