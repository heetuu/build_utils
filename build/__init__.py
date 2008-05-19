#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2007 All Rights Reserved  
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


def get_release():
    #get release info
    import release
    
    if release.identifier == "":
        raise RuntimeError, "release identifier not specified"

    return release


def build_release(releaser_root):
    'build a release'
    release = get_release()
    return _build( release, build_dirs( releaser_root ) )


def build_docs(releaser_root):
    'build a release'
    release = get_release()
    return _build( release, build_dirs( releaser_root ), args = ['docs'] )


def build_dirs( root, tmp = None, export = None, src = None, build = None ):
    '''create a data object to hold directories related to a build
    
    root: root directory of releaser
    tmp: tmporary path. usually $root/tmp
    export: root where binaries and python modules to be exported. usually $root/EXPORT
    src: path to the sources. usually $root/src
    '''
    if export is None: export = os.path.join( root, 'EXPORT' )
    if src is None: src = os.path.join( root, 'src' )
    if tmp is None: tmp = os.path.join(  root, 'tmp' )
    if build is None: build = os.path.join(tmp, 'build' )

    from BuildDirs import BuildDirs
    return BuildDirs( root, src, export, build, tmp)


def _build(release, builddirs, args = []):
    '''build

    builddirs: directories of the build (instance of BuildDirs)
    '''
    
    from packages import packageInfoTable
    config_dir = os.path.join( builddirs.src, packageInfoTable['config']['path'] )

    import build
    succeeded = False
    while not succeeded:
        try:
            build.run(
                release.name, builddirs.src, builddirs.export,
                builddirs.build, config_dir,
                arguments = args)
            succeeded = True
        except build.DependencyMissing, dep:
            print "Trying to install dependency '%s' ..." % dep
            from deps import install
            install( str(dep) )
            pass
        continue

    clean_up( builddirs.export )
    return


def clean_up( export_root, patterns = [ '.svn', 'CVS', '.pyc' ] ):
    for pattern in patterns: prune( export_root, pattern )
    return


def prune( path, pattern ):
    cmd = r'find "%s" -name "%s" -exec rm -rf {} \;' % (
        path, pattern )
    print "running %r..." % cmd
    os.system( cmd )
    return


import sys, os
import utils.installers



# version
__id__ = "$Id$"

# End of file 
