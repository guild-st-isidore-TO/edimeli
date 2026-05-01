# Editoris Melicorum (EMEL)

Editors of Melodies - GSI's music typesetting toolkit

---

> STATUS (XXVIII Aprilis MMXXVI)  
Active Development -- Refactoring this into a Poetry project for better portability and collaboration

![Editoris Melicorum mascot image](./docs/static/edi_melicorum_pic.png "Editoris Melicorum mascot image")

EdiMeli is a digital music typesetting toolkit for music ministries in Catholic parishes. The toolkit helps build musical arrangements around traditional hymns in Gregorian notation. As well as laying them out into documents, both for the congregation and the choir/musicians.

For more info, check out [this PDF handout on `EMEL v0.0.7`](./docs/static/emel-antiphons-1.1.pdf)

### Examples

Different sheet types for the same hymn:

1. [Complete guitar](./docs/static/marian-antiphons-simple-all-v0.8.pdf)
1. [Guitar accompanist](./docs/static/marian-antiphons-simple-accomp-v0.8.pdf)
1. [Guitar soloist](./docs/static/marian-antiphons-simple-solo-v0.8.pdf)

## LOCAL USAGE

### `poetry install`

Sets up the project

### `poetry run translate-all`

Translates all the contents of the `input/` directory, organized by folder.

Finished documents are sent to the `output/` directory, organized with the same folder names that were passed in.

### Setup

#### Requirements

**gabctk** `v240107` -- GABC conversion toolkit

https://github.com/jperon/gabctk/blob/master/README-en.md

**LilyPond** `v2.25.13` -- Digital music typesetting  
https://lilypond.org/download.html

#### Suggestions

**Frescobaldi** -- Lilypond viewer and editor

https://github.com/frescobaldi/frescobaldi/wiki

## CONFIGURATION

Configurations can be done in `edimeli.config.json`

### gabctk

The `paths` object in the config file looks like:

```json
"paths": {
    "gabctkDirectory": "../gabctk",
    "outputDirectoryLy": "output/ly",
    "outputDirectoryMidi": "output/midi",
    "outputDirectoryPdf": "output/pdf",
    "outputDirectoryXml": "output/xml"
}
```

The `gabctkDirectory` needs to be configured to point to a local instance/clone of `gabctk`. See repo: https://github.com/jperon/gabctk

## CONTRIBUTING

Want to contribute to the _Editoris_ project? Shoot an email to `salvador.workshop@gmail.com`

## Notes

- The ``(`)`` symbol in GABC input code causes errors in `gabctk`, and should be removed
