\bookpart {
  \pointAndClickOff

  \header {

    title = \markup \center-column {
      \vspace #3
      \abs-fontsize #26 "TemplateDocTitleLat"
      \vspace #1
      \abs-fontsize #24 \with-color #(x11-color 'grey35) \italic "TemplateDocTitle"

      \vspace #2.5
      \abs-fontsize #22 "TemplateDocPartLat"
      \vspace #0.5
      \abs-fontsize #22 "pro Vox et Cithara Hispanica"

      \vspace #1.5
      \abs-fontsize #21 \with-color #(x11-color 'grey35) \italic "TemplateDocPart"
      \vspace #0.5
      \abs-fontsize #21 \with-color #(x11-color 'grey35) \italic "for Voice and Spanish (Classical) Guitar"
    }

    subtitle = \markup \center-column {
      \vspace #3
      \abs-fontsize #16 "ex Fabrica Salvadoris et Collegium Sancti Isidori (TO)"
      \vspace #0.3
      \abs-fontsize #15 \with-color #(x11-color 'grey35) \italic "from Salvador Workshop and the Guild of St. Isidore (TO)"
    }

    EngravingCredLat = \markup { excudit Editoris Melicorum, per LilyPond v. #(lilypond-version) }
    EngravingCred = \markup { engraved by Editoris Melicorum, using LilyPond version #(lilypond-version) }

    subsubtitle = \markup \center-column {
      \vspace #1
      \abs-fontsize #14 \EngravingCredLat
      \vspace #0.3
      \abs-fontsize #14 "faciebat Torontinum (Canada) MMXXV"
      \vspace #0.3
      \abs-fontsize #14 "versio TemplateDocVersionLat"

      \vspace #1
      \abs-fontsize #13 \with-color #(x11-color 'grey35) \italic \EngravingCred
      \vspace #0.3
      \abs-fontsize #13 \with-color #(x11-color 'grey35) \italic "made in Toronto (Canada), 2025"
      \vspace #0.3
      \abs-fontsize #13 \with-color #(x11-color 'grey35) \italic "version TemplateDocVersion"
    }
  }

  \markup \vspace #2
  \markup \wordwrap {
    This file was generated through \bold "Editoris Melicorum"
    \italic "(Publishers of Music/Melodies)," a software project by
    \italic "Salvador Workshop" and the \italic "Guild of St. Isidore (TO)"
  }

  \markup \vspace #1
  \markup \wordwrap {
    Editoris Melicorum is a digital music typesetting toolkit for music ministries in Catholic parishes.
    The toolkit helps build musical arrangements around traditional hymns in Gregorian notation.
    As well as laying them out into documents, both for the congregation and the choir/musicians.
  }

  \markup \vspace #1
  \markup \wordwrap {
    For more information, the project's code repository is at: \bold https://github.com/guild-st-isidore-TO/editorismelicorum
  }
}
