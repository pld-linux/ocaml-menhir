#
# Conditional build:
%bcond_without	ocaml_opt	# skip building native optimized binaries (bytecode is always built)

# not yet available on x32 (ocaml 4.02.1), update when upstream will support it
%ifnarch %{ix86} %{x8664} arm aarch64 ppc sparc sparcv9
%undefine	with_ocaml_opt
%endif

%define		module	menhir
Summary:	LR(1) parser generator for the OCaml programming language
Name:		ocaml-%{module}
Version:	20170509
Release:	1
License:	GPL v2
Group:		Libraries
Source0:	http://gallium.inria.fr/~fpottier/menhir/%{module}-%{version}.tar.gz
# Source0-md5:	b8ba18b5abda831cf41cd4fa65f4c51b
URL:		http://gallium.inria.fr/~fpottier/menhir/
BuildRequires:	ocaml >= 3.04-7
BuildRequires:	ocaml-ocamlbuild
%requires_eq	ocaml-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		debug_package	%{nil}
%if %{without ocaml_opt}
%define		no_install_post_strip	1
# no opt means no native binary, stripping bytecode breaks such programs
%define		_enable_debug_packages	0
%endif

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
%requires_eq ocaml

%description devel
This package contains files needed to develop OCaml programs using
menhir.

%prep
%setup -q -n %{module}-%{version}

%build
%{__make} PREFIX=%{_prefix} USE_OCAMLFIND=true all

%install
rm -rf $RPM_BUILD_ROOT
export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml
install -d $OCAMLFIND_DESTDIR $OCAMLFIND_DESTDIR/stublibs
%{__make} install \
	PREFIX=%{_prefix} \
	DESTDIR=$RPM_BUILD_ROOT

# move to dir pld ocamlfind looks
install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/menhir{Lib,Sdk}
mv $OCAMLFIND_DESTDIR/menhirLib/META \
	$RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/menhirLib
cat <<EOF >> $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/menhirLib/META
directory="+menhirLib"
EOF

mv $OCAMLFIND_DESTDIR/menhirSdk/META \
	$RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/menhirSdk
cat <<EOF >> $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/menhirSdk/META
directory="+menhirSdk"
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc manual.pdf
%attr(755,root,root) %{_bindir}/menhir
%dir %{_libdir}/ocaml/%{module}*
%dir %{_datadir}/menhir
%{_datadir}/menhir/standard.mly
%{_mandir}/man1/menhir.1*

%files devel
%defattr(644,root,root,755)
%doc LICENSE
%{_libdir}/ocaml/menhirLib/menhirLib.ml
%{_libdir}/ocaml/%{module}*/*.cmi
%{_libdir}/ocaml/%{module}*/*.cmo
%{_libdir}/ocaml/%{module}*/*.mli
%if %{with ocaml_opt}
%{_libdir}/ocaml/%{module}*/*.[ao]
%{_libdir}/ocaml/%{module}*/*.cmx
%endif
%{_libdir}/ocaml/site-lib/%{module}*
