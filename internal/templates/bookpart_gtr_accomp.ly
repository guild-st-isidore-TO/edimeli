\bookpart {
  \pointAndClickOff

  \paper {
    left-margin = 0.8125\in
  }
  
  \header {
    title = "TemplateTitle"
    subtitle = \markup \italic { "TemplateSubtitle - TemplateInstrument" }
    composer = "TemplateComposer"
    arranger = "TemplateArranger"
    meter = "lib. info: TemplateDatabase"
  }

  \tocItem \markup { \bold "TemplateTitle" — \italic "TemplateSubtitle, TemplateInstrument" }
  \score{
    <<
      \new Staff <<
        \set Staff.instrumentName = "Voice"
        \set Staff.shortInstrumentName = "Vox"
        \set Staff.midiInstrument = "flute"
        \set Staff.autoBeaming = ##f
        \new Voice = "TemplateLyricsLink" {
          \cadenzaOn \transpose c TemplateTransposeKey{ \stemUp \TemplateVocals }
        }
      >>
      \new Lyrics \lyricsto TemplateLyricsLink {
        \TemplateLyrics
      }
      \new Staff \with {
        instrumentName = "Gtr (accomp.)"
        shortInstrumentName = "Gt-A"
      } {
        \clef "G_8"
        \cadenzaOn \transpose c TemplateTransposeKey{ \TemplateGuitarAccomp }
      }
    >>
    \layout{
      \context {
        \Staff
        \override VerticalAxisGroup.default-staff-staff-spacing.padding = #6
        \override TimeSignature #'stencil = #point-stencil
        \override Slur #'stencil = ##f
      }
    }
  }
}