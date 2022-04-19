%bcond_without tests
%bcond_without weak_deps

%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
%global __provides_exclude_from ^/opt/ros/humble/.*$
%global __requires_exclude_from ^/opt/ros/humble/.*$

Name:           ros-humble-rosidl-generator-py
Version:        0.14.2
Release:        2%{?dist}%{?release_suffix}
Summary:        ROS rosidl_generator_py package

License:        Apache License 2.0
Source0:        %{name}-%{version}.tar.gz

Requires:       python%{python3_pkgversion}-numpy
Requires:       ros-humble-ament-cmake
Requires:       ros-humble-ament-index-python
Requires:       ros-humble-python-cmake-module
Requires:       ros-humble-rmw
Requires:       ros-humble-rosidl-cli
Requires:       ros-humble-rosidl-cmake
Requires:       ros-humble-rosidl-generator-c
Requires:       ros-humble-rosidl-parser
Requires:       ros-humble-rosidl-runtime-c
Requires:       ros-humble-rosidl-typesupport-c
Requires:       ros-humble-rosidl-typesupport-interface
Requires:       ros-humble-rpyutils
Requires:       ros-humble-ros-workspace
BuildRequires:  ros-humble-ament-cmake
BuildRequires:  ros-humble-rosidl-runtime-c
BuildRequires:  ros-humble-ros-workspace
Provides:       %{name}-devel = %{version}-%{release}
Provides:       %{name}-doc = %{version}-%{release}
Provides:       %{name}-runtime = %{version}-%{release}
Provides:       ros-humble-rosidl-generator-packages(member)

%if 0%{?with_tests}
BuildRequires:  python%{python3_pkgversion}-numpy
BuildRequires:  python%{python3_pkgversion}-pytest
BuildRequires:  ros-humble-ament-cmake-pytest
BuildRequires:  ros-humble-ament-index-python
BuildRequires:  ros-humble-ament-lint-auto
BuildRequires:  ros-humble-ament-lint-common
BuildRequires:  ros-humble-python-cmake-module
BuildRequires:  ros-humble-rmw
BuildRequires:  ros-humble-rosidl-cmake
BuildRequires:  ros-humble-rosidl-generator-c
BuildRequires:  ros-humble-rosidl-generator-cpp
BuildRequires:  ros-humble-rosidl-parser
BuildRequires:  ros-humble-rosidl-typesupport-c
BuildRequires:  ros-humble-rosidl-typesupport-fastrtps-c
BuildRequires:  ros-humble-rosidl-typesupport-introspection-c
BuildRequires:  ros-humble-rpyutils
BuildRequires:  ros-humble-test-interface-files
%endif

%if 0%{?with_weak_deps}
Supplements:    ros-humble-rosidl-generator-packages(all)
%endif

%description
Generate the ROS interfaces in Python.

%prep
%autosetup -p1

%build
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/humble/setup.sh" ]; then . "/opt/ros/humble/setup.sh"; fi
mkdir -p .obj-%{_target_platform} && cd .obj-%{_target_platform}
%cmake3 \
    -UINCLUDE_INSTALL_DIR \
    -ULIB_INSTALL_DIR \
    -USYSCONF_INSTALL_DIR \
    -USHARE_INSTALL_PREFIX \
    -ULIB_SUFFIX \
    -DCMAKE_INSTALL_PREFIX="/opt/ros/humble" \
    -DAMENT_PREFIX_PATH="/opt/ros/humble" \
    -DCMAKE_PREFIX_PATH="/opt/ros/humble" \
    -DSETUPTOOLS_DEB_LAYOUT=OFF \
%if !0%{?with_tests}
    -DBUILD_TESTING=OFF \
%endif
    ..

%make_build

%install
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/humble/setup.sh" ]; then . "/opt/ros/humble/setup.sh"; fi
%make_install -C .obj-%{_target_platform}

%if 0%{?with_tests}
%check
# Look for a Makefile target with a name indicating that it runs tests
TEST_TARGET=$(%__make -qp -C .obj-%{_target_platform} | sed "s/^\(test\|check\):.*/\\1/;t f;d;:f;q0")
if [ -n "$TEST_TARGET" ]; then
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/humble/setup.sh" ]; then . "/opt/ros/humble/setup.sh"; fi
CTEST_OUTPUT_ON_FAILURE=1 \
    %make_build -C .obj-%{_target_platform} $TEST_TARGET || echo "RPM TESTS FAILED"
else echo "RPM TESTS SKIPPED"; fi
%endif

%files
/opt/ros/humble

%changelog
* Tue Apr 19 2022 Michel Hidalgo <michel@ekumenlabs.com> - 0.14.2-2
- Autogenerated by Bloom

* Tue Mar 01 2022 Michel Hidalgo <michel@ekumenlabs.com> - 0.14.2-1
- Autogenerated by Bloom

* Tue Feb 08 2022 Michel Hidalgo <michel@ekumenlabs.com> - 0.14.1-2
- Autogenerated by Bloom

