alfred-turbofilm-workflow
=========================

Alfred 2 workflow, which allows to search through unwatched episodes on turbofilm.tv

Usage
=========================

First you need to authenticate at turbofilm:

`tfauth username password`

Authentication cookies are stored, so you don't need to re-authenticate again.

After that the following commands are available:

| Command | Description |
|:-----|:----------------|
| `tfmy` | lists all series with unwatched episodes |
| `tfmy search_value` | filters list of series from above |
| `tfmy series_id` | lists first unwatched episodes from a certain series |

When you pick any episode, default browser with selected episode will be opened.
