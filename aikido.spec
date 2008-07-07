%define aikido_libdir %_prefix/lib/aikido/
%define aikido_platlibdir %_libdir/aikido/
%define aikido_includedir %_includedir/aikido/

Name: aikido
Version: 1.40
Release: %mkrel 2
License: Sun Public License
Group: Development/Other
Summary: A interpreted and object-oriented language with C++ semantics
URL: http://aikido.sf.net/
Source: http://downloads.sourceforge.net/aikido/aikido-%{version}_src.zip
Patch1: aikido-1.40-missing-includes.patch
Patch2: aikido-1.40-find-modules-paths.patch
BuildRequires: glib-devel
BuildRequires: gtk-devel
BuildRequires: gcc-c++
BuildRequires: libpcre-devel
BuildRequires: zip
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

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
%patch1 -p1
%patch2 -p1
cp %_sourcedir/aikido-gtk.c %_builddir/%name-%version

%build
# creates a dummy proxy module that links with libgtk-1.2.so.x.y.z
%__cc -shared -fPIC `gtk-config --cflags` `gtk-config --libs` \
	 -o libgtk.so aikido-gtk.c

export CPPFLAGS="`glib-config --cflags` '-DINSTALLDIR=\"%{aikido_platlibdir}:%{aikido_libdir}\"'"
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

install -d $RPM_BUILD_ROOT/%aikido_platlibdir
mv libgtk.so $RPM_BUILD_ROOT/%aikido_platlibdir
mv $RPM_BUILD_ROOT/%_libdir/{libddk.so,libdtk.so} \
	$RPM_BUILD_ROOT/%aikido_platlibdir

%files
%doc README CHANGES COPYRIGHT examples
%defattr(-,root,root,-)
%{aikido_libdir}/aikido.zip
%{aikido_platlibdir}/libgtk.so
%{aikido_platlibdir}/libddk.so
%{aikido_platlibdir}/libdtk.so
%_bindir/aikido
%_bindir/aikido_o
%_bindir/mkelf
%_bindir/mkstandalone
%_bindir/aikido-config
%_libdir/libaikidomath.so
%_libdir/libaikidonetwork.so
%_libdir/libaikidosecurity.so

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

