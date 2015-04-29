"""
@file
@brief Set up a jenkins server with all the necessary job
"""
import os
import sys

from pyquickhelper import noLOG


def setup_jenkins_server(js,
                         github="sdpython",
                         modules=[ ("pyquickhelper", "H H(10-11) * * 0"),
                                      ["pymyinstall", ],
                                      ["pymyinstall [anaconda] [update]",
                                          "pymyinstall [anaconda2] [update27]"],
                                      ["pyquickhelper [anaconda]", "pyquickhelper [winpython]",
                                          "pyquickhelper [27] [anaconda2]"],
                                      ["pyensae", ],
                                      ["pymmails", "pysqllike", "pyrsslocal", "pymyinstall [27] [anaconda2]",
                                       "python3_module_template", "pyensae [anaconda]", "pyensae [winpython]"],
                                      ["pymmails [anaconda]", "pysqllike [anaconda]", "pyrsslocal [anaconda]",
                                       "python3_module_template [anaconda]", "python3_module_template [27] [anaconda]",
                                       "pymyinstall [all]"],
                                      # actuariat 
                                      [("actuariat_python", "H H(12-13) * * 0")],
                                      ["actuariat_python [winpython]",
                                       "actuariat_python [anaconda]"],
                                      # code_beatrix
                                      ("code_beatrix", "H H(14-15) * * 0"),
                                      ["code_beatrix [winpython]",
                                       "code_beatrix [anaconda]"],
                                      # teachings
                                      ("ensae_teaching_cs", "H H(15-16) * * 0"),
                                      ["ensae_teaching_cs [winpython]",
                                       "ensae_teaching_cs [anaconda]"],
                                      "ensae_teaching_cs [notebooks]",
                                      ["ensae_teaching_cs [winpython] [notebooks]",
                                       "ensae_teaching_cs [anaconda] [notebooks]", ],
                                      ],
                             pythonexe=os.path.dirname(sys.executable),
                             winpython=r"C:\WinPython-64bit-3.4.3.2FlavorRfull\python-3.4.3.amd64",
                             anaconda=r"c:\Anaconda3",
                             anaconda2=r"c:\Anaconda2",
                             overwrite=False,
                             location=None,
                             no_dep=False,
                             prefix="",
                             fLOG=noLOG,
                             dependencies={'pymyinstall': ['pyquickhelper'],
                                           'pyensae': ['pyquickhelper'],
                                           'python3_module_template': ['pyquickhelper'],
                                           'ensae_teaching_cs': ['pyquickhelper', 'pyensae', 'pyrsslocal', 'pymmails'],
                                           'actuariat_python': ['pyquickhelper', 'pyensae', 'pyrsslocal', 'pymmails'],
                                           'code_beatrix': ['pyquickhelper', 'pyensae', 'pyrsslocal', 'pymmails'],
                                           },
                             platform=sys.platform):
    """
    Set up many jobs on Jenkins

    @param      js                  (JenkinsExt) jenkins server (specially if you need credentials)
    @param      github              github account if it does not start with *http://*, 
                                    the link to git repository of the project otherwise
    @param      modules             modules for which to generate the
    @param      get_jenkins_script  see @see me get_jenkins_script (default value if this parameter is None)
    @param      pythonexe           location of Python (unused)
    @param      winpython           location of WinPython (or None to skip)
    @param      anaconda            location of Anaconda (or None to skip)
    @param      overwrite           do not create the job if it already exists
    @param      location            None for default or a local folder
    @param      no_dep              if True, do not add dependencies
    @param      prefix              add a prefix to the name
    @param      dependencies        some modules depend on others also being tested,
                                    this parameter gives the list
    @param      platform            platform of the Jenkins server
    @param      fLOG                logging function
    @return                         list of created jobs
    
    *modules* is a list defined as follows:
    
        * each element can be a string or a tuple (string, schedule time) or a list
        * if it is a list, it contains a list of elements defined as previously
        * the job at position i is not scheduled, it will start after the last
          job at position i-1 whether or not it fails
          
    Example ::
    
         modules=[ ("pyquickhelper", "H H(10-11) * * 0"),
                  ["pymyinstall", ],
                  ["pymyinstall [anaconda] [update]",
                      "pymyinstall [anaconda2] [update27]"],
                  ["pyquickhelper [anaconda]", "pyquickhelper [winpython]",
                      "pyquickhelper [27] [anaconda2]"],
                  ["pyensae", ],
                  ["pymmails", "pysqllike", "pyrsslocal", "pymyinstall [27] [anaconda2]",
                   "python3_module_template", "pyensae [anaconda]", "pyensae [winpython]"],
                  ["pymmails [anaconda]", "pysqllike [anaconda]", "pyrsslocal [anaconda]",
                   "python3_module_template [anaconda]", "python3_module_template [27] [anaconda]",
                   "pymyinstall [all]"],
                  # actuariat 
                  [("actuariat_python", "H H(12-13) * * 0")],
                  ["actuariat_python [winpython]",
                   "actuariat_python [anaconda]"],
                  # code_beatrix
                  ("code_beatrix", "H H(14-15) * * 0"),
                  ["code_beatrix [winpython]",
                   "code_beatrix [anaconda]"],
                  # teachings
                  ("ensae_teaching_cs", "H H(15-16) * * 0"),
                  ["ensae_teaching_cs [winpython]",
                   "ensae_teaching_cs [anaconda]"],
                  "ensae_teaching_cs [notebooks]",
                  ["ensae_teaching_cs [winpython] [notebooks]",
                   "ensae_teaching_cs [anaconda] [notebooks]", ],
                  ],
    

    Example::

        from ensae_teaching_cs.automation.jenkins_helper import setup_jenkins_server, JenkinsExt

        js = JenkinsExt('http://machine:8080/', "user", "password")

        if True:
            js.setup_jenkins_server(github="sdpython",
                                modules=modules,
                                anaconda=r"C:\\Anaconda3",
                                anaconda2=r"C:\\Anaconda2",
                                winpython=r"C:\WinPython-64bit-3.4.3.2FlavorRfull\python-3.4.3.amd64",
                                fLOG=print,
                                overwrite = True,
                                location = r"c:\\jenkins\\pymy")


    For WinPython, version 3.4.3+ is mandatory to get the latest version of IPython (3).

    Another example::

        import sys
        sys.path.append(r"C:\<path>\ensae_teaching_cs\src")
        sys.path.append(r"C:\<path>\pyquickhelper\src")
        sys.path.append(r"C:\<path>\pyensae\src")
        sys.path.append(r"C:\<path>\pyrsslocal\src")
        from ensae_teaching_cs.automation.jenkins_helper import setup_jenkins_server, JenkinsExt
        js = JenkinsExt("http://<machine>:8080/", <user>, <password>)
        setup_jenkins_server(js,
                location=r"c:\jenkins\pymy",
                overwrite=True,
                fLOG=print)
    """
    r = js.setup_jenkins_server(github=github,
                             modules=modules,
                             get_jenkins_script=None,
                             pythonexe=pythonexe,
                             winpython=winpython,
                             anaconda=anaconda,
                             anaconda2=anaconda,
                             overwrite=overwrite,
                             location=location,
                             no_dep=no_dep,
                             prefix=prefix,
                             fLOG=fLOG,
                             dependencies=dependencies,
                             platform=platform)
    return r
                             
