%define aikido_libdir %_prefix/lib/aikido/
%define aikido_includedir %_includedir/aikido/

Name: aikido
Version: 1.40
Release: %mkrel 1
License: Sun Public License
Group: Development/Other
Summary: A interpreted and object-oriented language with C++ semantics
URL: http://aikido.sf.net/
Source: http://downloads.sourceforge.net/aikido/aikido-%{version}_src.zip
Patch0: aikido-1.40-find-systemzip-on-usrlib.patch
Patch1: aikido-1.40-missing-includes.patch
BuildRequires: glib-devel
BuildRequires: gtk-devel
BuildRequires: gcc-c++
BuildRequires: libpcre-devel
BuildRequires: zip

%description
Aikido is a relatively new programming language that can be used for rapid
scripting, prototyping and general programming tasks. 

It is a dynamically typed, object oriented language with built-in
multithreading. In some respects it is similar in functionality to Python,
Perl, JavaScript and Java. Syntactically it is very similar to C++ and
Java.

%package devel
Group: Development/Other
Summary: Libraries and headers needed to build Aikido modules

%description devel
Aikido is a relatively new programming language that can be used for rapid
scripting, prototyping and general programming tasks. 

This package contains the libraries and headers needed to build modules for
Aikido.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
#FIXME just use -DINSTALLDIR
sed -i 's,__MANDRIVA_INSTALLDIR__,"%{aikido_libdir}",g' src/site.h

export CPPFLAGS="`glib-config --cflags`"
make

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/usr
make install dest=$RPM_BUILD_ROOT/%{_prefix}

# the install script will always place in lib/
mv $RPM_BUILD_ROOT/%_prefix/lib $RPM_BUILD_ROOT/%_libdir/ || :

# it will be stripped anyway:
rm -f $RPM_BUILD_ROOT/%_bindir/aikido_g

install -d $RPM_BUILD_ROOT/%aikido_libdir
mv $RPM_BUILD_ROOT/%_bindir/aikido.zip $RPM_BUILD_ROOT/%aikido_libdir

install -d $RPM_BUILD_ROOT/%aikido_includedir
mv $RPM_BUILD_ROOT/%_includedir/*.h $RPM_BUILD_ROOT/%_includedir/unix \
	$RPM_BUILD_ROOT/%aikido_includedir

%files
%doc README CHANGES COPYRIGHT examples
%defattr(-,root,root,-)
%{aikido_libdir}/aikido.zip
%_bindir/aikido
%_bindir/aikido_o
%_bindir/mkelf
%_bindir/mkstandalone
%_bindir/aikido-config
%_libdir/libaikidomath.so
%_libdir/libaikidonetwork.so
%_libdir/libaikidosecurity.so
%_libdir/libddk.so
%_libdir/libdtk.so

%files devel
%{aikido_includedir}/aikido.h
%{aikido_includedir}/aikidotoken.h
%{aikido_includedir}/aikidozip.h
%{aikido_includedir}/aikidopcreposix.h
%{aikido_includedir}/aikidointerpret.h
%{aikido_includedir}/aikidocodegen.h
%{aikido_includedir}/aikidodebug.h
%{aikido_includedir}/unix/os.h
%_libdir/libaikido_o.a
%_libdir/libaikidosecurity.a
%_libdir/libaikidonetwork.a
%_libdir/libaikido_g.a
%_libdir/libaikidomath.a

