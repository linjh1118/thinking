\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{bytedance_seed}[2026/05/23 ByteDance Seed research template]
\LoadClassWithOptions{article}
\pdfoutput=1

% Page layout and typography
\RequirePackage[top=2.75cm, bottom=2.5cm, left=2.5cm, right=2.5cm, columnsep=0.65cm]{geometry}
\RequirePackage{microtype}
\RequirePackage{parskip}
\RequirePackage[latin, english]{babel}
\RequirePackage[T1]{fontenc}
\RequirePackage{hyphenat}

% Figures, floats, tables, and captions
\RequirePackage{graphicx}
\RequirePackage{booktabs}
\RequirePackage{caption}
\RequirePackage{placeins}
\RequirePackage[most]{tcolorbox}
\RequirePackage{xcolor}

% References
\RequirePackage{hyperref}
\RequirePackage[noabbrev,nameinlink]{cleveref}
\RequirePackage[numbers,sort&compress]{natbib}

% Header and visual details
\RequirePackage{etoolbox}
\RequirePackage{fancyhdr}
\RequirePackage{pifont}
\RequirePackage{titlesec}

\definecolor{seedbg}{HTML}{2E5AA8}
\definecolor{seedblue}{HTML}{2E5AA8}
\newcommand{\seedblue}[1]{{\bfseries\color{seedblue}#1}}

\hypersetup{
  colorlinks,
  linkcolor=seedblue,
  citecolor=seedblue,
  urlcolor=seedblue
}

\def\bibfont{\small}
\addto{\captionsenglish}{\renewcommand{\refname}{References}}

\newcommand{\sectionfont}{\fontsize{12}{10}\selectfont}
\newcommand{\subsectionfont}{\fontsize{11}{10}\selectfont}
\titleformat*{\paragraph}{\itshape}
\titleformat*{\section}{\sectionfont\sffamily\bfseries\seedblue}
\titleformat*{\subsection}{\subsectionfont\sffamily\bfseries\seedblue}
\titleformat*{\subsubsection}{\normalsize\sffamily\bfseries\seedblue}

\newcommand{\bffont}{\fontsize{8.8}{10}\selectfont}
\DeclareTextFontCommand{\textbf}{\bffont\bfseries\sffamily}

\DeclareCaptionLabelSeparator{custom}{}
\DeclareCaptionFormat{custom}{{\sffamily\textbf{#1 #2}} #3}
\captionsetup{singlelinecheck=true,format=custom,labelsep=custom,font=small}
\captionsetup[sub]{singlelinecheck=true,format=custom,labelsep=custom,font=small}

% ByteDance Seed fonts. Keep the seed/ directory with this class.
\DeclareFontFamily{T1}{bytesans}{}
\DeclareFontShape{T1}{bytesans}{m}{n}{<-> s * [1] seed/bytesans}{}
\pdfmapline{+bytesans < seed/ByteSans-Bold.ttf <T1-WGL4.enc}
\renewcommand{\sfdefault}{bytesans}

\DeclareFontFamily{T1}{bytesansmedium}{}
\DeclareFontShape{T1}{bytesansmedium}{m}{n}{<-> s * [1] seed/bytesansmedium}{}
\pdfmapline{+bytesansmedium < seed/ByteSans-Medium.ttf <T1-WGL4.enc}
\renewcommand{\rmdefault}{cmr}

% Title-page data helpers
\newcommand\seedaddtolist[5][]{%
  \begingroup
    \if\relax#3\relax\def\sep{}\else\def\sep{#5}\fi
    \let\protect\@unexpandable@protect
    \xdef#3{\expandafter{#3}\sep #4[#1]{#2}}%
  \endgroup
}

\newcommand{\authorfont}{\fontsize{12}{14}\selectfont}
\newcommand\authorlist{}
\newcommand\authorformat[2][]{\authorfont{\sffamily #2$^{#1}$}}
\renewcommand\author[2][]{\seedaddtolist[#1]{#2}{\authorlist}{\authorformat}{, }}

\newcommand{\affiliationfont}{\fontsize{10}{12}\selectfont}
\newcommand\affiliationlist{}
\newcommand\affiliationformat[2][]{{\affiliationfont{\fontfamily{bytesansmedium}\selectfont $^{#1}$#2}}}
\newcommand\affiliation[2][]{\seedaddtolist[#1]{#2}{\affiliationlist}{\affiliationformat}{, }}

\newcommand{\contributionfont}{\fontsize{10}{12}\selectfont}
\newcommand\contributionlist{}
\newcommand\contributionformat[2][]{{\contributionfont $^{#1}$#2}}
\newcommand\contribution[2][]{\seedaddtolist[#1]{#2}{\contributionlist}{\contributionformat}{, }}

\newcommand{\checkdatafont}{\fontsize{7.92}{10}\selectfont}
\newcommand\checkdatalist{}
\newcommand\checkdataformat[2][]{{\small{\checkdatafont\sffamily\bfseries #1:} #2}}
\newcommand\checkdata[2][]{\seedaddtolist[#1]{#2}{\checkdatalist}{\checkdataformat}{\par}}

\newcommand{\abstractinfont}{\fontsize{10}{12}\selectfont}
\renewcommand{\abstract}[1]{\gdef\abstractlist{{\abstractinfont #1}}}
\newcommand{\abstractlist}{}
\newcommand{\email}[1]{\href{mailto:#1}{\texttt{#1}}}

\renewcommand\date[1]{\checkdata[Date]{#1}}
\newcommand\projectlead[1]{\checkdata[Project Lead]{#1}}
\newcommand\correspondence[1]{\checkdata[Correspondence]{#1}}

\newcommand{\titlefont}{\fontsize{17}{20}\selectfont}
\newcommand{\titlelist}{}
\renewcommand{\title}[1]{\gdef\titlelist{\titlefont{\sffamily #1}}}

\newcommand{\abstractfont}{\fontsize{12}{12}\selectfont}
\newcommand{\beginabstract}{\abstractfont{\sffamily\bfseries\seedblue{Abstract}\par}}
\newcommand{\beginappendix}{\appendix{\titlefont\sffamily\seedblue{Appendix}\par}}

% Set \renewcommand{\seedanceteambadge}{} in paper.tex to hide this badge.
\newcommand{\seedanceteambadge}{%
  \par\vskip 4mm
  \begingroup
  \centering
  \tcbox[
    enhanced,
    colback=seedblue,
    colframe=seedblue,
    coltext=white,
    boxrule=0pt,
    arc=2mm,
    left=6mm,
    right=6mm,
    top=1.4mm,
    bottom=1.4mm,
    boxsep=0pt
  ]{\sffamily\bfseries\footnotesize \ding{72}\;\,Seedance Team Research Project\,\;\ding{72}}%
  \par
  \endgroup
}

\fancypagestyle{firststyle}{
  \fancyhead{}
  \fancyfoot{}
  \fancyhead[L]{\vskip 4mm\includegraphics[width=53.3mm,height=6mm]{seed/seed_logo.png}}
}

\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}

\newcommand{\@toptitlebar}{
  \seedblue{\hrule height 0.5pt}
  \vskip 6mm
}

\newcommand{\@bottomtitlebar}{
  \vskip 6mm
  \seedblue{\hrule height 0.5pt}
}

\newcommand{\mymaketitle}{%
  \tcbset{
    enhanced,
    left=8mm,
    right=8mm,
    top=6mm,
    bottom=6mm,
    colback=white,
    colframe=seedbg,
    boxrule=0.5pt,
    before skip=0pt,
    grow to left by=1.5pt,
    grow to right by=1.5pt,
    arc=2.5mm
  }
  {
    \setlength{\parskip}{0mm}
    \centering
    \nohyphens
    \@toptitlebar
    \titlelist\par
    \@bottomtitlebar
    \vskip 6mm
    \authorlist
    \vskip 3mm
    \affiliationlist\par
    \vskip 3mm
    \contributionlist\par
  }
  \vskip 6mm
  \begin{tcolorbox}
    \setlength{\parindent}{0cm}
    \setlength{\parskip}{0cm}
    \begin{center}
      \beginabstract
      \vskip 3mm
    \end{center}
    \abstractlist\par
    \vskip 3mm
    {
      \setlength{\parskip}{0cm}
      \ifdefempty{\checkdatalist}{\vspace*{0.65cm}}{\checkdatalist\par}
    }
    \seedanceteambadge
  \end{tcolorbox}
  \tcbset{reset}
  \FloatBarrier
  \thispagestyle{firststyle}
}

\if@twocolumn
\renewcommand{\maketitle}{%
  \twocolumn[
    \vskip 3mm
    \mymaketitle
    \vskip 8mm
  ]%
}
\else
\renewcommand{\maketitle}{%
  \mymaketitle
  \vskip 8mm
}
\fi
