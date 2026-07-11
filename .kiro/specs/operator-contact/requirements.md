# Requirements Document

## Introduction

This feature updates the OKS Suv Telegram bot so users can reach a human operator directly by phone. It covers three changes: adding a new administrator Telegram ID to the environment configuration, renaming the existing "Support" menu button to "Contact Operator" across all supported languages, and showing a tappable phone number when the button is pressed so the user can place a call to the operator directly. The bot supports three languages (Uzbek, Russian, English), so all user-facing text introduced or changed by this feature must be localized in each language.

## Glossary

- **Bot**: The OKS Suv Telegram bot application built on aiogram.
- **Config_Loader**: The component in `bot/config.py` that reads environment variables and exposes them as Python values, including `ADMIN_TELEGRAM_IDS`.
- **Admin_ID_List**: The `ADMIN_TELEGRAM_IDS` list of administrator Telegram user IDs, sourced from the `ADMIN_TELEGRAM_IDS` environment variable.
- **New_Admin_ID**: The administrator Telegram ID `8816532579` to be added to the Admin_ID_List.
- **Localization_Store**: The `TRANSLATIONS` dictionary in `bot/localization.py` accessed through the `get_text` function.
- **Main_Keyboard**: The main reply keyboard returned by `get_main_keyboard` in `bot/keyboards/reply.py`.
- **Operator_Button**: The main-menu button previously labeled "Support" (`btn_support`), to be relabeled "Contact Operator".
- **Operator_Phone_Number**: The publicly displayed phone number a user calls to reach the operator.
- **Operator_Handler**: The message handler in `bot/handlers/start.py` triggered when a user presses the Operator_Button.
- **Supported_Language**: One of the three languages the Bot supports: Uzbek (`uz`), Russian (`ru`), English (`en`).
- **Operator_Contact_Message**: The localized message shown to the user containing the tappable Operator_Phone_Number.

## Requirements

### Requirement 1: Add new administrator ID to configuration

**User Story:** As a bot owner, I want an additional administrator Telegram ID registered in the configuration, so that the new operator receives administrator messages and support notifications.

#### Acceptance Criteria

1. WHEN the Config_Loader initializes at application startup and the `ADMIN_TELEGRAM_IDS` environment variable contains the value `8816532579`, THE Config_Loader SHALL include the New_Admin_ID `8816532579` as an integer entry in the Admin_ID_List.
2. WHEN the Config_Loader adds the New_Admin_ID to the Admin_ID_List, THE Config_Loader SHALL retain every administrator ID already present in the `ADMIN_TELEGRAM_IDS` environment variable, so that the resulting Admin_ID_List count equals the number of distinct valid IDs supplied.
3. WHEN the `ADMIN_TELEGRAM_IDS` environment variable contains between 2 and 100 comma-separated IDs, THE Config_Loader SHALL parse each ID into a separate integer entry in the Admin_ID_List, preserving the left-to-right order in which the IDs appear in the variable.
4. IF an entry in the `ADMIN_TELEGRAM_IDS` environment variable is empty or contains only whitespace between separators, THEN THE Config_Loader SHALL exclude that entry from the Admin_ID_List and SHALL include all remaining valid IDs.
5. IF an entry in the `ADMIN_TELEGRAM_IDS` environment variable cannot be converted to an integer after trimming surrounding whitespace, THEN THE Config_Loader SHALL exclude that entry from the Admin_ID_List, SHALL emit a warning-level log indicating the rejected value, and SHALL continue processing the remaining entries.
6. IF the `ADMIN_TELEGRAM_IDS` environment variable is unset or empty, THEN THE Config_Loader SHALL produce an empty Admin_ID_List.

### Requirement 2: Rename the Support button to Contact Operator

**User Story:** As a bot user, I want the main-menu button to read "Contact Operator", so that I understand I can reach a human operator directly.

#### Acceptance Criteria

1. THE Localization_Store SHALL provide the Operator_Button label text "Operator bilan bog'lanish" for the Uzbek language.
2. THE Localization_Store SHALL provide the Operator_Button label text "Связаться с оператором" for the Russian language.
3. THE Localization_Store SHALL provide the Operator_Button label text "Contact Operator" for the English language.
4. THE Localization_Store SHALL provide exactly one non-empty Operator_Button label, between 1 and 64 characters in length, for each Supported_Language.
5. WHERE a user has selected a Supported_Language, THE Main_Keyboard SHALL display the Operator_Button label in that Supported_Language.
6. IF a user has not selected a Supported_Language, THEN THE Main_Keyboard SHALL display the Operator_Button label in the default Supported_Language (Uzbek).
7. WHEN a user presses the Operator_Button in any Supported_Language, THE Operator_Handler SHALL be triggered exactly once.
8. IF the Operator_Handler fails to complete after being triggered, THEN THE Bot SHALL send a user-facing error message and SHALL preserve the Main_Keyboard.

### Requirement 3: Display a tappable operator phone number

**User Story:** As a bot user, I want to see a tappable phone number when I press "Contact Operator", so that I can call the operator directly from Telegram.

#### Acceptance Criteria

1. WHEN a registered user presses the Operator_Button, THE Bot SHALL send the Operator_Contact_Message containing the Operator_Phone_Number within 3 seconds of receiving the button press.
2. THE Operator_Contact_Message SHALL present the Operator_Phone_Number in international format beginning with a "+" country code and containing only digits after the "+", so that Telegram renders it as a tap-to-call link.
3. WHERE a registered user has previously selected a Supported_Language, THE Bot SHALL send the Operator_Contact_Message in that Supported_Language.
4. IF a registered user presses the Operator_Button and has not previously selected a Supported_Language, THEN THE Bot SHALL send the Operator_Contact_Message in the default Supported_Language.
5. WHEN a registered user presses the Operator_Button, THE Bot SHALL display the Main_Keyboard together with the Operator_Contact_Message in a single response.
6. IF an unregistered user presses the Operator_Button, THEN THE Bot SHALL send the registration-prompt message instructing the user to run `/start`, and THE Bot SHALL NOT send the Operator_Contact_Message.
7. IF sending the Operator_Contact_Message fails, THEN THE Bot SHALL retry sending up to 2 additional times, and IF all attempts fail, THEN THE Bot SHALL send an error message indicating the operator contact could not be delivered.
