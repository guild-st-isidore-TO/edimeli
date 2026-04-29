\bookpart {
  \pointAndClickOff

  \paper {
    left-margin = 0.8125\in
    system-system-spacing.padding = #6

    % system-system-spacing =
    %   #'((basic-distance . 12) 
    %      (minimum-distance . 8)
    %      (padding . 4)
    %      (stretchability . 60)) 
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
      \new Lyrics = "mlyrics"
      \new Staff <<
        \set Staff.instrumentName = "Gtr (solo)"
        \set Staff.shortInstrumentName = "Gt-S"
        \set Staff.autoBeaming = ##f

        \clef "G_8"
        \new Voice = "TemplateLyricsLink" {
          \cadenzaOn \transpose c TemplateTransposeKey{ \stemUp \TemplateGuitarSolo }
        }
      >>
      \context Lyrics = "mlyrics" {
        \lyricsto TemplateLyricsLink {
          \TemplateLyrics
        }
      }
    >>
    \layout{
      \context {
        \Staff
        \override TimeSignature #'stencil = #point-stencil
        \override Slur #'stencil = ##f
      }
    }
  }
}