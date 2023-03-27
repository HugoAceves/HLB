% FCFMTESIS.CLS
%
%(c) Álvaro Castañeda Mendoza
%(C) Honorina Ruíz Estrada
%(c) COORDINCACIÓN DEL COLEGIO DE FÍSICA DE LA FCFM
% Este programa no tiene garantía, y las personas mencionadas arriba
% no se hacen responsables por los daños causados por el mal uso de
% este programa.
%
%PROHIBIDA TODA MODIFICACIÓN A ESTE ARCHIVO EXCEPTO POR SUS AUTORES O
%EL ENCARGADO DE MANTENER ESTE PAQUETE QUIEN ÚNICAMENTE PUEDE SER
%DESIGNADO POR LA COORDINACIÓN DEL COLEGIO DE FÍSICA O LA DIRECCIÓN DE
%LA FACULTAD DE CIENCIAS FÍSICO-MATEMÁTICAS DE LA BENÉMERITA
%UNIVERSIDAD AUTÓNOMA DE PUEBLA.
%
%SI SE MODIFICA ESTE ARCHIVO DEBERÁ SER CAMBIADO SU NOMBRE Y NO PODRÁ
%SER UTILIZADO PARA ESCRIBIR TESIS EN LA FCFM. SI ALGUIEN DESEA
%UTILIZARLO PARA ESCRIBIR TESIS FUERA DE LA FCFM DEBERÁ CONSERVAR TODO ESTE
%TEXTO, Y AGREGAR EN LAS LÍNEAS INDICADAS QUE ES UNA MODIFICACIÓN DE
%FCFMTESIS.CLS, INCLUIR LOS NOMBRES DE LOS AUTORES ORIGINALES Y DE
%PREFERENCIA PONERSE EN CONTACTO CON LOS AUTORES ORIGINALES, DE ESTA
%MANERA SE PUEDE HACER UNA MODIFICACIÓN A ESTE ARCHIVO PARA INCLUIR
%LOS INTERESES PARTICULARES A SU FACULTAD O COLEGIO, Y TENER UN
%FORMATO COMÚN PARA TODOS.
%
%%% 17/12/2001 v3.3 Tesis para la FCFM
%%% 19/09/12 JMHL, v 3.4.4, añadí la información para que sirva para
%%% una tesis de maestría y doctorado en el Posgrado de Física Aplicada
%%% 13/11/14 JMHL, cambio a la nueva versión del escudo,
%%% manejo estándar de UTF8, pdflatex
%%% 15/01/18 JMHL, v 3.4.5, todas las opciones de grados de la FCFM
%%% 15/06/18 JMHL, v 3.4.6, revisión y adecuación de los ejemplos
%%% 26/01/19 Mónica Macías (MM), v 3.4.7, agregado de dos instrucciones 
%%% para compilar con latexml
%%% 20/06/19 MM, corrección de numeración romana en el frontmatter,
%%% corrección de mensajes en warnings, minúsculas por mayúsculas,
%%% cambió Alumno por Estudiante, agregado de es-tabla en el paquete babel
%%% para renombrar correctamente 'Cuadro' por 'Tabla' sin usar renewcommand,
%%% borrado de líneas comentadas e instrucciones innecesarias
%%% 13/11/19 se eliminaron las opciones pma1 y pma2 que hacían referencia
%%% a tesis de maestría y doctorado respectivamente en el Posgrado en Mat.

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{fcfmtesis}[2018/01/15 v3.4.5 Estilo de documento para tesis de la FCFM-BUAP]

\DeclareOption{fisica}
    {\newcommand\colegio{\textsf{\textbf{Colegio de F\'\i sica}}}%
     \newcommand\grado{\textbf{\textsc{Licenciado en F\'\i sica}}}}
\DeclareOption{fisapl}
    {\newcommand\colegio{\textsf{\textbf{Colegio de F\'\i sica}}}%
     \newcommand\grado{\textbf{\textsc{Licenciado en F\'\i sica Aplicada}}}}
\DeclareOption{pfa1}
    {\newcommand\colegio{\textsf{\textbf{Posgrado en F\'\i sica Aplicada}}}%
     \newcommand\grado{\textbf{\textsc{Maestro en Ciencias}}}}
\DeclareOption{pfa2}
    {\newcommand\colegio{\textsf{\textbf{Posgrado en F\'\i sica Aplicada}}}%
     \newcommand\grado{\textbf{\textsc{Doctor en Ciencias}}}}
\DeclareOption{matematicas}
    {\newcommand\colegio{\textsf{\textbf{Colegio de Matem\'aticas}}}%
     \newcommand\grado{\textbf{\textsc{Licenciado en Matem\'aticas}}}}
\DeclareOption{lma}
    {\newcommand\colegio{\textsf{\textbf{Colegio de Matem\'aticas}}}%
     \newcommand\grado{\textbf{\textsc{Licenciado en Matem\'aticas Aplicadas}}}}
\DeclareOption{actuaria}
    {\newcommand\colegio{\textsf{\textbf{Colegio de Matem\'aticas}}}%
     \newcommand\grado{\textbf{\textsc{Licenciado en Actuar\'\i a}}}}
\DeclareOption{mem}
    {\newcommand\colegio{\textsf{\textbf{Posgrado de Educaci\'on Matem\'atica}}}%
     \newcommand\grado{\textbf{\textsc{Maestro en Educación Matem\'aticas}}}}

 \DeclareOption*{\PassOptionsToClass{\CurrentOptions}{book}}
 \DeclareOption*{\ClassWarning{fcfmtesis}{Opción desconocida: \CurrentOption}}
 \ProcessOptions\relax
 
 \LoadClass[letterpaper,10pt,twoside,titlepage,openright,onecolumn,final]{book}
 
 \RequirePackage[spanish, es-tabla]{babel}
 \RequirePackage{latexsym}
 \RequirePackage{fancyhdr}
 \RequirePackage{graphicx}
 \RequirePackage{array}
 
 \def\asesor#1{\gdef\@asesor{#1}}
 \def\@asesor{\@latex@warning@no@line{No me has dado al \noexpand\asesor}}
 \def\presidente#1{\gdef\@presidente{#1}}
 \def\@presidente{\@latex@warning@no@line{No me has dado al \noexpand\presidente}}
 \def\secretario#1{\gdef\@secretario{#1}}
 \def\@secretario{\@latex@warning@no@line{No me has dado al \noexpand\secretario}}
 \def\vocala#1{\gdef\@vocala{#1}}
 \def\@vocala{\@latex@warning@no@line{No me has dado al \noexpand\vocala}}
 \def\vocalb#1{\gdef\@vocalb{#1}}
 \def\@vocalb{\@latex@warning@no@line{No me has dado al \noexpand\vocalb}}
 \def\hombre{\gdef\@asesorad{Asesorado por}}
 \def\mujer{\gdef\@asesorad{Asesorada por}}
 \def\@asesorad{\@latex@warning@no@line{No se si eres hombre o mujer. %
 Usa \@backslashchar hombre o \@backslashchar mujer}\stop}
 \def\trabajo{Tesis }
 \def\tesina{\renewcommand{\trabajo}{Tesina }}

 \newsavebox{\escudo}
 \sbox{\escudo}{\includegraphics[scale=.8]{images/escudo.png}}
 \newcommand\escudoBUAP{\usebox{\escudo}}

 \newcommand\portada{%
 	\begin{titlepage}%
    	\def\@thanks{}
  		\let\footnotesize\small
  		\let\footnoterule\relax
  		\let\footnote\null
  		\let\footnotemark\null
  		\null\vfil
  		%\vskip 20\p@
  		\begin{center}%
  			\begin{flushleft}
   				\begin{tabular}{cp{15cm}}
   					\begin{picture}(0,0)(0,2.5)%
             			\put(-2.2,.1){\escudoBUAP}
   					\end{picture}
					& {\huge Benem\'erita Universidad Aut\'onoma de Puebla \par}%
  					  {\rule{13.5cm}{1pt}}%
  					  \vskip 1.5em%
    				  {\huge Facultad de Ciencias F\'\i sico Matem\'aticas \par}
  					  {\rule{12cm}{1pt}}%
            	\end{tabular}
            \end{flushleft}
			\vskip 3em%
			%\null\vfill
    		{\LARGE \@title \par}%
    		\vskip 3em%
    		{\Large \trabajo presentada al \par}%
    		\vskip 1em%
    		{\Large \colegio \par}%
    		\vskip 1em%
    		{\Large como requisito parcial para la obtenci\'on del  grado de \par}%
    		\vskip 1em%
    		{\Large \grado \par}%
    		\vskip 1em%
    		{\Large por \par}%
    		\vskip 1em%
    		{\Large \@author \par}%
            \vskip 3em%
            {\Large \@asesorad\par}%
            \vskip 2em%
            {\Large Carlos Arturo Hernández Gracidas y  \@asesor \par }%
    		\vskip 3em%
            
    		{Puebla Pue. \par}%
   			 %\vskip 3em%
    		{  \@date\par}%
		\end{center}\par
 		% {\null\@thanks\par}
  		\vfil\null
        \let\thanks\relax
	\end{titlepage}
 }

 \renewcommand\maketitle{%
	\begin{titlepage}%
        \def\@thanks{}
  		\let\footnotesize\small
  		\let\footnoterule\relax
  		%\let\footnote\relax
  		\let\footnote\thanks
  		\null
  		%\vskip 20\p@
		\begin{center}%
  			\begin{flushleft}
   				\begin{tabular}{cp{15cm}}
   					\begin{picture}(0,0)(0,2.5)%
             			\put(-2.2,.1){\escudoBUAP}
   					\end{picture}
					& {\huge Benem\'erita Universidad Aut\'onoma de Puebla \par}%
  					{\rule{13.5cm}{1pt}}%
  					\vskip 1.5em%
    				{\huge Facultad de Ciencias F\'\i sico Matem\'aticas \par}
  					{\rule{12cm}{1pt}}%
             	\end{tabular}
			\end{flushleft}
			\vskip 3em%
			%\null\vfill
    		{\LARGE \@title \par}%
    		\vskip 3em%
    		{\Large Tesis presentada al \par}%
    		\vskip 1em%
    		{\Large \colegio \par}%
    		\vskip 1em%
    		{\Large como requisito parcial para la obtenci\'on del  grado de \par}%
    		\vskip 1em%
    		{\Large \grado \par}%
    		\vskip 1em%
    		{\Large por \par}%
    		\vskip 1em%
    		{\Large \@author \par}%
            \vskip 3em%
            {\Large \@asesorad\par}%
            \vskip 2em%
            {\Large Carlos Arturo Hernández Gracidas y \@asesor \par}% 
			\vskip 3em%
    		{Puebla Pue. \par}%
    		%\vskip 3em%
    		{  \@date\par}%
		\end{center}\par
  		{\@thanks\par}
  		\vfil\null%
        \let\thanks\relax
	\end{titlepage}%
 }

 \newcommand\makeacta{
	\begin{titlepage}%
		\def\@thanks{}%evita la ocurrencia de doble pie de página
		\let\footnotesize\small
		\let\footnoterule\relax
		\let\footnote\thanks %\relax
		%\let \mpfootnotetext{}
		\null\vfill
		%\vskip 60\p@
  		\begin{flushleft}%
			{\Large \textbf{T\'\i tulo:} \@title \par}
            %\let\@thanks\relax
       		{\Large \textbf{Estudiante:} \textsc{\@author} \par}%
   		\end{flushleft}%
   	
   		\vspace{1cm}
     	\begin{center}
     		\large
       		COMIT\'E
       		
       		\vspace{1.2cm}%
       		\rule{5cm}{1pt}%
       		
       		\@presidente
       		
       		Presidente
       		
       		\vspace{1.2cm}%
       		\rule{5cm}{1pt}%
       		
       		\@secretario
       	
       		Secretario
       		
       		\vspace{1.2cm}%
       		\rule{5cm}{1pt}%
       		
       		\@vocala
       		
       		Vocal
            
            
       		
       		\vspace{1.2cm}%
       		\rule{5cm}{1pt}%
       		
       		\@asesor
       		
       		 Asesor
       		 
       		\vspace{1.2cm}%
       		\rule{5cm}{1pt}%
       		
       		Carlos Arturo Hernández Gracidas
       		
       		 Asesor
		\end{center}
        \@thanks\par
     	\vfill\null
		% \@thanks\par
		%
 		%  {\@thanks\par}%
	\end{titlepage}%
 }

\long\def\@footnotetext#1{\insert\footins{%
	\reset@font\footnotesize
    \interlinepenalty\interfootnotelinepenalty
    \splittopskip\footnotesep
    \splitmaxdepth \dp\strutbox \floatingpenalty \@MM
    \hsize\columnwidth \@parboxrestore
    \protected@edef\@currentlabel{%
       \csname p@footnote\endcsname\@thefnmark
    }%
    \color@begingroup
      \@makefntext{%
        \rule\z@\footnotesep\ignorespaces#1\@finalstrut\strutbox}%
    \color@endgroup}}%

\def\footnotemark{%
	\@ifnextchar[\@xfootnotemark
    {\stepcounter{footnote}%
    \protected@xdef\@thefnmark{\thefootnote}%
    \@footnotemark}}

\def\footnote{\@ifnextchar[\@xfootnote{\stepcounter\@mpfn
	\protected@xdef\@thefnmark{\thempfn}%
    \@footnotemark\@footnotetext}}

\renewcommand\footnoterule{%
	\kern-3\p@
  	\hrule\@width.4\columnwidth
  	\kern2.6\p@}

\@addtoreset{footnote}{chapter}

\sloppy
\setlength{\unitlength}{1cm}
\setlength{\evensidemargin}{0cm}
\setlength{\oddsidemargin}{.5in}
\setlength{\footskip}{1cm}
\setlength{\headheight}{10mm}
\setlength{\headsep}{5mm}
\setlength{\marginparwidth}{0cm}
\setlength{\marginparsep}{0cm}
\setlength{\marginparpush}{0cm}
\setlength{\topmargin}{0cm}
\setlength{\textheight}{22cm}
\setlength{\textwidth}{15cm}

%\pagestyle{fancy}
%\addtolenght{\headheight}{\baselineskip}%
\renewcommand{\chaptermark}[1]{\markboth{#1}{}}%
\renewcommand{\sectionmark}[1]{\markright{\thesection\ #1}}%
\rhead[{\bfseries\leftmark}\\\rightmark]{{\bfseries\leftmark}\\\rightmark}%
\lhead[]{}%
\chead[]{}%
\rfoot{}%
\cfoot{\thepage}%
\lfoot[]{}%
\renewcommand{\headrulewidth}{.5mm}%
\renewcommand{\footrulewidth}{.5mm}%

%Agregadas para que funcione latexml
\newif\if@openright \@openrighttrue
\newif\if@mainmatter \@mainmattertrue \@mainmatterfalse

\renewcommand\chapter{%
	\if@openright\cleardoublepage\else\clearpage\fi
    \thispagestyle{plain}%
    \global\@topnum\z@
    \@afterindentfalse
    \secdef\@chapter\@schapter}

\def\@chapter[#1]#2{%
	\ifnum \c@secnumdepth >\m@ne
      \if@mainmatter
        \refstepcounter{chapter}%
        \typeout{\@chapapp\space\thechapter.}%
        \addcontentsline{toc}{chapter}%
        {\protect\numberline{\thechapter}#1}%
      \else
        \addcontentsline{toc}{chapter}{#1}%
      \fi
    \else
      \addcontentsline{toc}{chapter}{#1}%
    \fi
    \chaptermark{#1}%
    \addtocontents{lof}{\protect\addvspace{10\p@}}%
    \addtocontents{lot}{\protect\addvspace{10\p@}}%
    \if@twocolumn
      \@topnewpage[\@makechapterhead{#2}]%
    \else
      \@makechapterhead{#2}%
      \@afterheading
    \fi}

\def\@makechapterhead#1{%
	\vspace*{50\p@}%
	{\parindent \z@ \raggedright \normalfont
	\ifnum \c@secnumdepth >\m@ne
	  \if@mainmatter
	    \huge\bfseries \@chapapp\space \thechapter
	    \par\nobreak
	    \vskip 25\p@
	  \fi
	\fi
	\interlinepenalty\@M
	\Huge \bfseries #1\par\nobreak
	\vskip 40\p@
	}}

\def\@schapter#1{%
	\if@twocolumn
	  \@topnewpage[\@makeschapterhead{#1}]%
	\else
	  \@makeschapterhead{#1}%
	  \@afterheading
	\fi}

\def\@makeschapterhead#1{%
	\vspace*{50\p@}%
	{\parindent \z@ \raggedright
	\normalfont
	\interlinepenalty\@M
	\Huge \bfseries  #1\par\nobreak
	\vskip 40\p@
	}}

\renewcommand\mainmatter{%
	\if@openright
	  \cleardoublepage
	\else
	  \clearpage
	\fi
	\@mainmattertrue
	\pagenumbering{arabic}
	\pagestyle{fancy}
	}

\renewcommand\backmatter{%
	\if@openright
	 \cleardoublepage
	\else
	 \clearpage
	\fi
	\@mainmatterfalse
	\pagestyle{empty}
	}

%Esta parte corrige el error de tener el encabezado de el índice de
%    tablas después de \chapter*{}
%Lo que realmente hace es redefinir el comando \cleardoublepage de tal
%    forma que use el comando \thispagestyle{empty} en la página que va
%    antes de una nueva sección.
%Para mas informacion consultar el error latex/2803 en LaTeX bug database:
%    www.latex-project.org/cgi-bin/ltxbugs2html?introduction=yes&state=open
\renewcommand{\cleardoublepage}{\clearpage\if@twoside \ifodd\c@page\else
   \thispagestyle{empty}% <---
   \hbox{}\newpage\if@twocolumn\hbox{}\newpage\fi\fi\fi}


\endinput
