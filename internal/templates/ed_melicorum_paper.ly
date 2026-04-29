\paper {
  %% book paper, which is inherited by all children bookparts
  ragged-last-bottom = ##t
  
  %% Page footer: add a different part-tagline at part last page
  oddFooterMarkup = \markup {
    \column {
      \fill-line {
        %% Copyright header field only on book first page.
        \if \on-first-page \fromproperty #'header:copyright
      }
      \fill-line {
        %% Part tagline header field only on each part last page.
        \if \on-last-page-of-part \fromproperty #'header:parttagline
      }
      \fill-line {
        %% Tagline header field only on book last page.
        \if \on-last-page \fromproperty #'header:tagline
      }
    }
  }

  % There's a bug in Times New Roman font shipped by Apple. Gotta change it.
  % see https://stackoverflow.com/questions/79562896/why-would-lilypond-be-replacing-capital-n-in-lyrics-with-u1eca-latin-capital-l
  property-defaults.fonts.serif = "Garamond"
  % property-defaults.fonts.sans = "DejaVu Sans"
  % property-defaults.fonts.typewriter = "Courier New"

  left-margin = 0.625\in
  bottom-margin = 0.625\in
  right-margin = 0.625\in
  top-margin = 0.625\in

  tocItemMarkup = \tocItemWithDotsMarkup
}
