\version "2.24.4"

#(set-default-paper-size "letter")

\include "TemplateOutLocation/TemplateFilenameSlug_vocals.ly"
\include "TemplateOutLocation/TemplateFilenameSlug_lyrics.ly"
\include "TemplateOutLocation/TemplateFilenameSlug_gt_comp.ly"
\include "TemplateOutLocation/TemplateFilenameSlug_gt_solo.ly"

\book {

  %%------------------------------------
  %% Header & Paper Configurations

  \include "./editoris_melicorum_header.ly"
  \include "./editoris_melicorum_paper.ly"

  %%------------------------------------
  %% Title Page

  \include "TemplateOutLocation/TemplateFilenameSlug_title_gt_all.ly"
  
  %%------------------------------------
  %% Table of Contents, Preface

  \include "./editoris_melicorum_toc_preface.ly"

  %%------------------------------------
  %% Main Content

  \include "TemplateOutLocation/TemplateFilenameSlug_bkpts_gt_all.ly"

}
