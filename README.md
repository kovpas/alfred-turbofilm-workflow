alfred-turbofilm-workflow
=========================

Alfred 2 workflow, which allows to search through unwatched episodes on turbofilm.tv

Usage
=========================

First you need to authenticate at turbofilm:

`tfauth username password`

Authentication cookies are stored, so you don't need to re-authenticate again.

In case if you are already authenticated in safari, you may try to do

`tfauth -safari`

This command uses safari cookies for authentication.

Also you can check your authentication status with the following command:

`tfauth`

Growl or Mountain Lion notification will be shown with a corresponding status.

After that the following commands are available:

| Command | Description |
|:-----|:----------------|
| `tfmy` | lists all series with unwatched episodes |
| `tfmy search_value` | filters list of series from above |
| `tfmy series_id` | lists first unwatched episodes from a certain series |

When you pick any episode, default browser with selected episode will be opened.
