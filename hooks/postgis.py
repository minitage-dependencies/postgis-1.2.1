import shutil
import re
import os

from minitage.core.common import substitute

def pre_configure(options, buildout):
    cwd=buildout['buildout']['parts-directory']
    flex=buildout['flex']['location']
    libiconv=buildout['libiconv']['location']
    #os.environ['PATH'] = cwd+"/flex/bin/:"+ os.environ.get('PATH','')
    #os.environ['LD_LIBRARY_PATH'] = cwd+"/flex/lib/:"+ cwd+"/libiconv/lib/:"+os.environ.get('LD_LIBRARY_PATH','')
    os.environ['CFLAGS']="  -I%s/include -I%s/include"%(libiconv,flex)
    os.environ['CPPFLAGS']="-I%s/include -I%s/include"%(libiconv,flex)
    os.environ['CXXFLAGS']="-I%s/include -I%s/include"%(libiconv,flex)
    os.environ['LDFLAGS']= "-L%s/lib -Wl,-rpath -Wl,%s/lib -L%s/lib -Wl,-rpath -Wl,%s/lib"    %(libiconv,flex,libiconv,flex)
    if os.uname()[0] == 'Darwin':
        os.environ['LDFLAGS']= ' -mmacosx-version-min=10.5.0 ' + os.environ['LDFLAGS']

def pre_make(options, buildout):
    """Custom pre-make hook for patching PostGIS."""
    # ``make install`` fails because it tries to write files under
    # /etc. This will write under the corresponding parts directory
    # instead.
    substitute('extras/template_gis/Makefile',
               '\$\(DESTDIR\)',
               '$(prefix)')

    # Put in rpath info
    rpath = os.environ['LDFLAGS']
    substitute('Makefile.config',
               'DLFLAGS=-shared',
               'DLFLAGS=-shared %s' % rpath)

def pre_make_deb(options, buildout):
    """Custom pre-make hook for patching PostGIS."""
    # ``make install`` fails because it tries to write files under
    # /etc. This will write under the corresponding parts directory
    # instead.
    substitute('extras/template_gis/Makefile',
               '\$\(DESTDIR\)',
               '$(prefix)')
