\version "2.25.13"

#(set-default-paper-size "letter")

\include "TemplateOutLocation/TemplateFilenameSlug_vocals.ly"
\include "TemplateOutLocation/TemplateFilenameSlug_lyrics.ly"
\include "TemplateOutLocation/TemplateFilenameSlug_gt_comp.ly"
\include "TemplateOutLocation/TemplateFilenameSlug_gt_solo.ly"

\book {

  %%------------------------------------
  %% Header & Paper Configurations

  \include "./ed_melicorum_header.ly"
  \include "./ed_melicorum_paper.ly"

  %%------------------------------------
  %% Title Page

  \include "TemplateOutLocation/TemplateFilenameSlug_title_gt_accomp.ly"
  
  %%------------------------------------
  %% Table of Contents, Preface

  \include "./ed_melicorum_toc_preface.ly"

  %%------------------------------------
  %% Main Content

  \include "TemplateOutLocation/TemplateFilenameSlug_bkpts_gt_accomp.ly"

}
