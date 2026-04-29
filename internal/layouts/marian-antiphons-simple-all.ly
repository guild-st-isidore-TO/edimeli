\version "2.24.4"

#(set-default-paper-size "letter")

\include "../build/ly/marian_ant_sim_vocals.ly"
\include "../build/ly/marian_ant_sim_lyrics.ly"
\include "../build/ly/marian_ant_sim_gt_comp.ly"
\include "../build/ly/marian_ant_sim_gt_solo.ly"

\book {

  %%------------------------------------
  %% Header & Paper Configurations

  \include "./parts/editoris_melicorum_header.ly"
  \include "./parts/editoris_melicorum_paper.ly"

  %%------------------------------------
  %% Title Page

  \include "../build/ly/marian_ant_sim_title_gt_all.ly"
  
  %%------------------------------------
  %% Table of Contents, Preface

  \include "./parts/editoris_melicorum_toc_preface.ly"

  %%------------------------------------
  %% Main Content

  \include "../build/ly/marian_ant_sim_bkpts_gt_all.ly"

}
