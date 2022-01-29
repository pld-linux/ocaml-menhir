#
# Conditional build:
%bcond_without	ocaml_opt	# native optimized binaries (bytecode is always built)
%bcond_without	coq		# coq menhir library

# not yet available on x32 (ocaml 4.02.1), update when upstream will support it
%ifnarch %{ix86} %{x8664} %{arm} aarch64 ppc sparc sparcv9
%undefine	with_ocaml_opt
%undefine	with_coq
%endif

%if %{without ocaml_opt}
%define		_enable_debug_packages	0
%endif

%define		module	menhir
Summary:	LR(1) parser generator for the OCaml programming language
Name:		ocaml-%{module}
Version:	20210310
Release:	2
License:	GPL v2 (generator), LGPL v2 with linking exception (library)
Group:		Libraries
Source0:	https://gitlab.inria.fr/fpottier/menhir/-/archive/%{version}/menhir-%{version}.tar.bz2
# Source0-md5:	1a0388baec7a5ba7c931e074d2c322d7
URL:		http://gallium.inria.fr/~fpottier/menhir/
%{?with_coq:BuildRequires:	coq}
BuildRequires:	ocaml >= 3.04-7
BuildRequires:	ocaml-dune
%requires_eq	ocaml-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Menhir is a LR(1) parser generator for the OCaml programming language.
That is, Menhir compiles LR(1) grammar specifications down to OCaml
code.

Menhir is 90% compatible with ocamlyacc. Legacy ocamlyacc grammar
specifications are accepted and compiled by Menhir. The resulting
parsers run and produce correct parse trees. However, parsers that
explicitly invoke functions in module Parsing behave slightly
incorrectly. For instance, the functions that provide access to
positions return a dummy position when invoked by a Menhir parser.
Porting a grammar specification from ocamlyacc to Menhir requires
replacing all calls to module Parsing with new Menhir-specific
keywords.

%package devel
Summary:	Menhir development part
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%requires_eq	ocaml

%description devel
This package contains files needed to develop OCaml programs using
menhir.

%package -n coq-menhirlib
Summary:	Support library for verified Coq parsers produced by Menhir
License:	LGPL v3+
Requires:	coq

%description -n coq-menhirlib
The Menhir parser generator, in --coq mode, can produce Coq parsers.
These parsers must be linked against this library, which provides both
an interpreter (which allows running the generated parser) and a
validator (which allows verifying, at parser construction time, that
the generated parser is correct and complete with respect to the
grammar).

%prep
%setup -q -n %{module}-%{version}

%build
dune build --verbose %{?_smp_mflags}

%if %{with coq}
%{__make} -C coq-menhirlib \
	VERBOSE=1
%endif

%install
rm -rf $RPM_BUILD_ROOT

dune install \
	--verbose \
	--destdir=$RPM_BUILD_ROOT

%if %{with coq}
%{__make} -C coq-menhirlib install \
	DESTDIR=$RPM_BUILD_ROOT
%endif

# sources
%{__rm} $RPM_BUILD_ROOT%{_libdir}/ocaml/{menhirLib,menhirSdk}/*.ml
# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_prefix}/doc/{menhir*,coq-menhirlib}
%if %{without coq}
%{__rm} -r $RPM_BUILD_ROOT%{_libdir}/ocaml/coq-menhirlib
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE doc/manual.pdf
%attr(755,root,root) %{_bindir}/menhir
%dir %{_libdir}/ocaml/menhir
%{_libdir}/ocaml/menhir/META
%dir %{_libdir}/ocaml/menhirLib
%{_libdir}/ocaml/menhirLib/META
%{_libdir}/ocaml/menhirLib/*.cma
%dir %{_libdir}/ocaml/menhirSdk
%{_libdir}/ocaml/menhirSdk/META
%{_libdir}/ocaml/menhirSdk/*.cma
%if %{with ocaml_opt}
%attr(755,root,root) %{_libdir}/ocaml/menhirLib/*.cmxs
%attr(755,root,root) %{_libdir}/ocaml/menhirSdk/*.cmxs
%endif
%{_mandir}/man1/menhir.1*

%files devel
%defattr(644,root,root,755)
%{_libdir}/ocaml/menhir/dune-package
%{_libdir}/ocaml/menhirLib/dune-package
%{_libdir}/ocaml/menhirLib/*.cmi
%{_libdir}/ocaml/menhirLib/*.cmt
%{_libdir}/ocaml/menhirLib/*.cmti
%{_libdir}/ocaml/menhirLib/*.mli
%{_libdir}/ocaml/menhirSdk/dune-package
%{_libdir}/ocaml/menhirSdk/*.cmi
%{_libdir}/ocaml/menhirSdk/*.cmt
%{_libdir}/ocaml/menhirSdk/*.cmti
%{_libdir}/ocaml/menhirSdk/*.mli
%if %{with ocaml_opt}
%{_libdir}/ocaml/menhirLib/*.a
%{_libdir}/ocaml/menhirLib/*.cmx
%{_libdir}/ocaml/menhirLib/*.cmxa
%{_libdir}/ocaml/menhirSdk/*.a
%{_libdir}/ocaml/menhirSdk/*.cmx
%{_libdir}/ocaml/menhirSdk/*.cmxa
%endif

%if %{with coq}
%files -n coq-menhirlib
%defattr(644,root,root,755)
%doc coq-menhirlib/{CHANGES.md,LICENSE,README.md}
%dir %{_libdir}/ocaml/coq-menhirlib
%{_libdir}/ocaml/coq-menhirlib/META
%{_libdir}/ocaml/coq-menhirlib/dune-package
%{_libdir}/coq/user-contrib/MenhirLib
%endif
