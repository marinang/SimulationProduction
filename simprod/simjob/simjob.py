#!/usr/bin/python
# -*- coding: utf-8 -*-

# Author: Matthieu Marinangeli
# Mail: matthieu.marinangeli@cern.ch
# Description: simulation job class

import os
import time
from random import randint, shuffle
import warnings
import glob
from tqdm import tqdm
from colorama import Fore
import sys

from .setup import DoProd, checksiminputs
from .utils import *
from .utils.utilities import (
    green,
    red,
    blue,
    cyan,
    magenta,
    cdefault,
    baserunnumber,
    silentrm,
)
from .utils.Database import getdatabase
from .utils.Status import Status
from .utils.GetEvtType import getevttype
from .utils.MoveJobs import Move, EosMove
from .exceptions import JobNotPreparedError

from tinydb import Query

DATABASE, STORAGE = getdatabase()

DEBUG = 0

TIME_NEW = 20  # minutes, time between check of status if status is new
TIME_RUNNING = 5
TIME_FAILED = 5
TIME_SUBMITTED = 1

py3 = (
    sys.version_info[0] > 2
)  # creates boolean value for test that Python major version > 2


class JobCollection(object):
    """
    Container class of the SimulationJob
    """

    def __init__(self):

        self.jobs = {}
        n_jobs = len(self.collection)

        if IsHTCondor():
            from utils.HTCondorUtils import Scheduler

            self._job_kwargs = {"scheduler": Scheduler()}
        else:
            self._job_kwargs = {"scheduler": None}

        if n_jobs > 0:

            print(red("\nLoading Jobs:"))
            t = tqdm(total=n_jobs)

            for k in self.keys:

                job_k = self.collection.get(doc_id=k)

                if job_k["status"] == "completed":
                    self.jobs[k] = None
                else:
                    self.jobs[k] = SimulationJob.from_doc(job_k, **self._job_kwargs)

                t.update(1)

            t.close()

        self.update()

    @property
    def collection(self):
        """
        Returns the table 'jobs' in the databse
        """
        return DATABASE.table("jobs")

    @property
    def keys(self):
        """
        Returns keys of SimulationJob in the collection
        """
        return sorted([j.doc_id for j in self.collection.all()], key=int)

    def __str__(self):
        """
        Returns the str representation of the JobCollection, which is a str with
        one line per SimulationJob in the collection with the following description:
            * number/key
            * status
            * evttype
            * year
            * number of events
            * number of SimulationSubJob's
            * number of running SimulationSubJob's
            * number of completed SimulationSubJob's
            * number of failed SimulationSubJob's
        """

        self.update()

        toprint = []
        toprint.append("{0} jobs".format(len(self.jobs)))

        h_job = "    #job "
        h_status = "       status "
        h_evttype = "       evttype "
        h_year = "   year "
        h_nevents = "  #events "
        h_subjobs = "  #subjobs "
        h_running = "  #R "
        h_completed = "  #C "
        h_failed = "  #F "

        tojoin = [
            h_job,
            h_status,
            h_evttype,
            h_year,
            h_nevents,
            h_subjobs,
            h_running,
            h_completed,
            h_failed,
        ]
        header = "|".join(tojoin) + "|"
        line = "".join(["-" for i in range(len(header) - 2)])

        toprint.append(line)
        toprint.append(header)
        toprint.append(line)

        for k in self.keys:
            job = self.jobs[k]

            if job is not None:
                status = job.status
                evttype = job.evttype
                year = job.year
                nevents = job.nevents
                subjobs = job.nsubjobs
                if status == "new":
                    nrunning = 0
                    ncompleted = 0
                    nfailed = 0
                else:
                    nrunning = len(job.select("running"))
                    ncompleted = len(job.select("completed"))
                    nfailed = len(job.select("failed"))
            else:
                job_doc = self.collection.get(doc_id=k)
                status = job_doc["status"]
                evttype = job_doc["evttype"]
                year = job_doc["year"]
                nevents = job_doc["nevents"]
                subjobs = job_doc["nsubjobs"]
                nrunning = job_doc["nrunning"]
                ncompleted = job_doc["ncompleted"]
                nfailed = job_doc["nfailed"]

            if status == "submitted":
                color = cyan
            elif status == "new":
                color = cdefault
            elif status == "prepared":
                color = cdefault
            elif status == "submitting":
                color = magenta
            elif status == "running":
                color = green
            elif status == "completed":
                color = blue
            elif status == "failed":
                color = red

            p_job = "{n:{fill}{al}{w}} ".format(
                w=(len(h_job) - 1), al=">", fill="", n=k
            )

            p_status = "{n:{fill}{al}{w}} ".format(
                w=(len(h_status) - 1), al=">", fill="", n=status
            )

            p_evttype = "{n:{fill}{al}{w}} ".format(
                w=(len(h_evttype) - 1), al=">", fill="", n=evttype
            )

            p_year = "{n:{fill}{al}{w}} ".format(
                w=(len(h_year) - 1), al=">", fill="", n=year
            )

            p_nevents = "{n:{fill}{al}{w}} ".format(
                w=(len(h_nevents) - 1), al=">", fill="", n=nevents
            )

            p_subjobs = "{n:{fill}{al}{w}} ".format(
                w=(len(h_subjobs) - 1), al=">", fill="", n=subjobs
            )

            p_running = "{n:{fill}{al}{w}} ".format(
                w=(len(h_running) - 1), al=">", fill="", n=nrunning
            )

            p_completed = "{n:{fill}{al}{w}} ".format(
                w=(len(h_completed) - 1), al=">", fill="", n=ncompleted
            )

            p_failed = "{n:{fill}{al}{w}} ".format(
                w=(len(h_failed) - 1), al=">", fill="", n=nfailed
            )

            tojoin = [
                p_job,
                p_status,
                p_evttype,
                p_year,
                p_nevents,
                p_subjobs,
                p_running,
                p_completed,
                p_failed,
            ]

            linejob = "|".join(tojoin) + "|"

            toprint.append(color(linejob))

        toprint = "\n".join(toprint)

        return toprint

    def _repr_pretty_(self, p, cycle):
        """
        Method called in IPython to print the representation of the JobCollection
        """
        if cycle:
            p.text(self.__str__())
            return
        p.text(self.__str__())

    def __geti__(self, i, printlevel=1):
        """
        Methods to access the i-th SimulationJob in the collection. If the SimulationJob with key i is
        in the collection but not loaded it will be loaded. If the key is larger than the maximum key in the
        in the collection, the database gets updated to fetch newly created SimulationJob's in the simprod
        prompt.

        Args:
            * i (int): key of the SimulationJob to access
            * printlevel (int, default=1): if 1 the loading the of the SimulationJob is printed, if 0 nothing
                is printed

        Returns:
            SimulationJob

        Raises:
            KeyError if a SimulationJob with key = i is not in the collection
        """

        if i not in self.keys and i > max(self.keys):
            self.update()
        if i not in self.keys:
            raise KeyError("job {0} not found!".format(i))
        else:
            if self.jobs[i] is None:
                if printlevel > 0:
                    print(green("Loading Job {0}:".format(i)))
                job_i_doc = self.collection.get(doc_id=i)
                job_i = SimulationJob.from_doc(job_i_doc, **self._job_kwargs)
                self.jobs[i] = job_i

            new_to_prepared = (
                self.jobs[i].status == "new" and len(self.jobs[i].jobtable) > 0
            )
            prepared_to_new = (
                self.jobs[i].status == "prepared" and len(self.jobs[i].jobtable) == 0
            )

            if new_to_prepared or prepared_to_new:
                job_i_doc = self.collection.get(doc_id=i)
                self.jobs[i] = SimulationJob.from_doc(job_i_doc, **self._job_kwargs)

        return self.jobs[i]

    def __getitem__(self, i):
        """
        Methods to access the i-th SimulationJob in the collection.

        Args:
            * i (int): key of the SimulationJob to access

        Returns:
            SimulationJob

        Raises:
            KeyError if a SimulationJob with key = i is not in the collection
        """
        return self.__geti__(i, printlevel=1)

    def __iter__(self):
        """
        Iterates over the SimulationJob's in the collection
        """
        for k in self.keys:
            yield self.__geti__(k, printlevel=-1)

    def __len__(self):
        """
        Returns the number of SimulationJob in the collection
        """
        return len(self.collection)

    def select(self, status):
        """
        Selects all the SimulationJob's with the status given as arguments.

        Args:
            * status (str): the status of interest

        Returns:
            List[SimulationJob]
        """
        return [j for j in self.__iter__() if j.status == status]

    def update(self):
        """
        Method to update the table 'jobs' in the database.
        """

        if len(self.collection) > 0:
            condition = (Query().status == "new") | (Query().status == "submitting")
            condition = (
                condition
                | (Query().status == "submitted")
                | (Query().status == "prepared")
            )
            to_update = self.collection.search(condition)
        else:
            to_update = []

        for j in to_update:
            if j.doc_id not in self.jobs.keys():
                self.jobs[j.doc_id] = SimulationJob.from_doc(j, **self._job_kwargs)
            elif (
                len(self.jobs[j.doc_id].subjobs) == 0
                or len(self.jobs[j.doc_id].jobtable) == 0
            ):
                self.jobs[j.doc_id] = SimulationJob.from_doc(j, **self._job_kwargs)
            else:
                self.jobs[j.doc_id]._update_job_in_database(
                    update_subjobs_in_database=True
                )

        if len(self.jobs) > len(self.keys):
            for k in self.jobs.keys():
                if k not in self.keys:
                    del self.jobs[k]

        for k in self.keys:

            job_doc = self.collection.get(doc_id=k)

            if k not in self.jobs.keys():
                job = SimulationJob.from_doc(job_doc, **self._job_kwargs)
                self.jobs[k] = job
            else:
                job = self.jobs[k]

            if job is None:
                continue

            status = job.last_status
            if status != job_doc["status"]:
                _dict = dict(status=status)
                self.collection.update(_dict, doc_ids=[k])

            if status in ["completed", "failed"]:
                self.jobs[k] = None


class SimulationJob(object):
    """
    Simulation job
    """

    def __init__(
        self,
        nevents,
        year,
        evttype,
        neventsjob=50,
        polarities=None,
        simcond="Sim09h",
        stripping=None,
        turbo=False,
        mudst=False,
        runnumber=baserunnumber(),
        decfiles="v30r46",
        redecay=False,
        simmodel="pythia8",
        keeplogs=True,
        keepxmls=True,
        **kwargs
    ):
        self.subjobs = {}
        self._options = {}

        non_supported_kws = [{"supported": "polarities", "non_supported": ["polarity"]}]
        for nkws in non_supported_kws:
            for ns in nkws["non_supported"]:
                if ns in kwargs:
                    msg = "The keyword {kw_ns} is not supported, use {kw_s} instead."
                    msg = msg.format(kw_ns=ns, kw_s=nkws["supported"])
                    warnings.warn(blue(msg))

        self.nevents = nevents
        self.year = year
        self.decfiles = decfiles
        self.evttype = evttype
        self.neventsjob = neventsjob
        self.polarities = polarities
        self.simcond = simcond
        self._stripping = stripping
        self.turbo = turbo
        self.mudst = mudst
        self._runnumber = runnumber
        self.redecay = redecay
        self.simmodel = simmodel
        self.keeplogs = keeplogs
        self.keepxmls = keepxmls
        self._inscreen = kwargs.get("inscreen", False)
        self._status = "new"

        _basedir = os.getenv("SIMOUTPUT")
        if not _basedir:
            _basedir = os.getenv("HOME") + "/SimulationJobs"

        self._options["basedir"] = kwargs.get("basedir", _basedir)

        self.htcondor = False

        if IsSlurm():
            self._options["loginprod"] = True

        elif IsHTCondor() or IsLSF():
            if os.getenv("LOG_SIMOUTPUT"):
                self._options["loginprod"] = kwargs.get("loginprod", False)
            else:
                self._options["loginprod"] = kwargs.get("loginprod", True)

            if not self._options["loginprod"]:
                self._options["logdir"] = kwargs.get(
                    "logdir", os.getenv("LOG_SIMOUTPUT")
                )

        self.scheduler = kwargs.get("scheduler", None)

        if IsHTCondor():
            self.htcondor = True
            if self.scheduler is None:
                self.scheduler = Scheduler()

        self.deliveryclerk = DeliveryClerk(
            inscreen=self._inscreen, scheduler=self.scheduler
        )

        if not self.options.get("loginprod", True):
            self._options["logdestdir"] = "{0}/{1}".format(
                self.options["logdir"], self.subdir()
            )

        self.screensessions = []

        self.database = DATABASE

        self.jobnumber = None

        if kwargs.get("newjob", True):
            jobstable = self.database.table("jobs")
            jobstable.insert(self.outdict())
            self.jobnumber = jobstable._last_id
            if DEBUG > 0:
                print("newjob:", self.jobnumber)
        else:
            self.jobnumber = kwargs.get("jobnumber", None)

    @property
    def jobtable(self):
        return self.database.table("job_{}".format(self.jobnumber))

    @property
    def range_subjobs(self):
        for n in range(self.nsubjobs):
            yield n + 1

    @property
    def nevents(self):
        return self._nevents

    @nevents.setter
    def nevents(self, value):
        if isinstance(value, (int, float)):
            value = int(value)
            self._nevents = value

        else:
            raise TypeError("nevents must be a int!")

    @property
    def neventsjob(self):
        return self._neventsjob

    @neventsjob.setter
    def neventsjob(self, value):
        if isinstance(value, (int, float)):
            value = int(value)
            self._neventsjob = value
        else:
            raise TypeError("nevents must be a int!")

    @property
    def nsubjobs(self):
        self._nsubjobs = int(self.nevents / self.neventsjob)
        return self._nsubjobs

    @property
    def evttype(self):
        return self._evttype

    @evttype.setter
    def evttype(self, value):
        self._evttype = value
        self._setoptfile()

    @property
    def simcond(self):
        return self._simcond

    @simcond.setter
    def simcond(self, value):
        if not isinstance(value, str):
            raise TypeError(
                "{0} has a non valid {1} type for simcond, must be a str!".format(
                    value, type(value)
                )
            )
        if value not in ["Sim09b", "Sim09c", "Sim09e", "Sim09f", "Sim09h"]:
            raise ValueError(
                "simcond must be Sim09b, Sim09c, Sim09d, Sim09f or Sim09h!"
            )
        self._simcond = value

    @property
    def simmodel(self):
        return self._simmodel

    @simmodel.setter
    def simmodel(self, value):
        if not isinstance(value, str):
            raise TypeError(
                "{0} has a non valid {1} type for simmodel, must be a str!".format(
                    value, type(value)
                )
            )
        if value not in ["pythia8", "BcVegPy"]:
            raise ValueError("simmodel must be pythia8 or BcVegPy!")
        self._simmodel = value

    @property
    def doprod(self):
        return DoProd(self.simcond, self.year)

    @property
    def stripping(self):
        return self._stripping

    @stripping.setter
    def stripping(self, value):
        if not isinstance(value, str):
            raise TypeError(
                "{0} has a non valid {1} type for stripping, must be a str!".format(
                    value, type(value)
                )
            )
        if value not in [
            "21",
            "24",
            "28",
            "24r1",
            "24r1p1",
            "28r1",
            "28r1p1",
            "28r2",
            "29r2",
            "29r2p1",
            "34",
            "34r0p1",
        ]:
            raise ValueError(
                "stripping must be '21, '24', '28', '24r1', '24r1p1', '28r1', '28r1p1', '28r2', '29r2', '29r2p1', '34' or '34r0p1'!"
            )
        self._stripping = value

    @property
    def year(self):
        return self._year

    @year.setter
    def year(self, value):
        if not isinstance(value, int):
            raise TypeError(
                "{0} has a non valid {1} type for year, must be a int!".format(
                    value, type(value)
                )
            )
        if value not in [2011, 2012, 2015, 2016, 2017, 2018]:
            raise ValueError("year must be 2011, 2012, 2015, 2016, 2017 or 2018!")
        self._year = value

    @property
    def polarities(self):
        return self._polarities

    @polarities.setter
    def polarities(self, value):
        if value is None:
            self._polarities = value
        elif isinstance(value, str):
            if value not in ["MagUp", "MagDown"]:
                msg = "Invalid value '{}' for polarities. Valid choices are ['MagUp', 'MagDown'].".format(
                    value
                )
                raise ValueError(msg)
            else:
                self._polarities = value
        else:
            msg = "Invalid {} type for polarities. A None value or a str equals to 'MagUp' or 'MagDown' is required."
            raise TypeError(msg.format(type(value)))

    @property
    def keys(self):
        return self.subjobs.keys()

    @property
    def options(self):
        return self._options

    def subdir(self):
        subdir = "simProd_{0}_{1}".format(self.evttype, self.simcond)
        if self.turbo:
            subdir += "_Turbo"
        if self.mudst:
            subdir += "_muDST"
        if self.redecay:
            subdir += "_ReDecay"

        self.options["subdir"] = subdir

        return subdir

    @property
    def proddir(self):
        self._proddir = "{0}/{1}".format(self.options["basedir"], self.subdir())
        return self._proddir

    @property
    def destdir(self):
        self._destdir = "{0}/{1}/{2}/{3}".format(
            self.options["basedir"], self.evttype, self.year, self.simcond
        )
        if self._redecay:
            self._destdir += "_ReDecay"
        return self._destdir

    @property
    def optfile(self):
        return self._optfile

    @property
    def turbo(self):
        return self._turbo

    @turbo.setter
    def turbo(self, value):
        if isinstance(value, bool):
            self._turbo = value
        else:
            raise TypeError(
                "{0} has a non valid {1} type for turbo, must be a bool!".format(
                    value, type(value)
                )
            )

    @property
    def mudst(self):
        return self._mudst

    @mudst.setter
    def mudst(self, value):
        if isinstance(value, bool):
            self._mudst = value
        else:
            raise TypeError(
                "{0} has a non valid {1} type for mudst, must be a bool!".format(
                    value, type(value)
                )
            )

    @property
    def decfiles(self):
        return self._decfiles

    @decfiles.setter
    def decfiles(self, value):
        if isinstance(value, str):
            self._decfiles = value
        else:
            raise TypeError(
                "{0} has a non valid {1} type for decfiles, must be a str!".format(
                    value, type(value)
                )
            )

    @property
    def redecay(self):
        return self._redecay

    @redecay.setter
    def redecay(self, value):
        if isinstance(value, bool):
            self._redecay = value
        else:
            raise TypeError(
                "{0} has a non valid {1} type for redecay, must be a bool!".format(
                    value, type(value)
                )
            )

    @property
    def keeplogs(self):
        return self._keeplogs

    @keeplogs.setter
    def keeplogs(self, value):
        if isinstance(value, bool):
            self._keeplogs = value
        else:
            raise TypeError(
                "{0} has a non valid {1} type for keeplogs, must be a bool!".format(
                    value, type(value)
                )
            )

    @property
    def keepxmls(self):
        return self._keepxmls

    @keepxmls.setter
    def keepxmls(self, value):
        if isinstance(value, bool):
            self._keepxmls = value
        else:
            raise TypeError(
                "{0} has a non valid {1} type for keepxmls, must be a bool!".format(
                    value, type(value)
                )
            )

    def getrunnumber(self, job_number=None):
        if job_number is not None and not isinstance(job_number, int):
            raise TypeError(
                "Job number must be a 'int'. Got a '{0}' instead!".format(
                    job_number.__class__.__name__
                )
            )

        if job_number is None:
            return self._runnumber
        else:
            return self._runnumber + job_number

    def prepare(self, update_table=True, **kwargs):
        if len(self.subjobs) < 1:

            if not self._evttype:
                raise ValueError("Evttype not defined!")

            if not self._nevents:
                raise ValueError("nevents not defined!")

            if not self._neventsjob:
                raise ValueError("neventsjob not defined!")

            if not self._year:
                raise ValueError("year not defined!")

            if not self._simcond:
                raise ValueError("simcond not defined!")

            checksiminputs(self)

            if self.nsubjobs == 0:

                self.neventsjob = int(self.nevents / 2)
                self.nevents = self.neventsjob * 2

            def sample_polarities():
                polarities = ["MagUp", "MagDown"]
                i = randint(0, 1)
                p1 = polarities.pop(i)
                p2 = polarities[0]

                polarity = [p1 for i in range(1, int(self.nsubjobs / 2) + 1)]
                polarity += [
                    p2 for i in range(int(self.nsubjobs / 2) + 1, self.nsubjobs + 1)
                ]
                return shuffle(polarity)

            if not isinstance(self._polarities, list):
                if self._polarities is None:
                    self._polarities = sample_polarities()
                elif self._polarities in ["MagUp", "MagDown"]:
                    self._polarities = [self._polarities for i in self.range_subjobs]
                else:
                    raise ValueError(
                        "Invalid value '{}' for polarities. Valid choices are ['MagUp', 'MagDown']".format(
                            self._polarities
                        )
                    )
            else:
                if len(self._polarities) != self.nsubjobs:
                    self._polarities = sample_polarities()
                elif not all(p in ["MagUp", "MagDown"] for p in self._polarities):
                    raise ValueError("Invalid values for polarities.")

        infiles = kwargs.get("infiles", [])

        for n in self.range_subjobs:
            if self.subjobs.get(n, None) is not None:
                continue

            self._preparesubjobs(n, infiles=infiles)

        self._status == "prepared"

        if update_table:
            self._update_job_in_database(update_subjobs_in_database=True)

    def _preparesubjobs(self, sjn, **kwargs):
        if DEBUG > 2:
            print(sjn)

        if self._polarities:
            polarity = self._polarities[sjn - 1]
        else:
            if sjn <= int(self.nsubjobs / 2):
                polarity = "MagUp"
            else:
                polarity = "MagDown"

        if sjn not in self.keys:
            runnumber = self.getrunnumber(sjn)
            self.subjobs[sjn] = SimulationSubJob(
                parent=self,
                polarity=polarity,
                runnumber=runnumber,
                subjobnumber=sjn,
                **kwargs
            )

    def send(self, job_number=None):

        if self.status == "completed":
            print("Job is completed. There is nothing to send.")
        else:
            failedsubjobs = self.select("failed")

            if len(failedsubjobs) > 0:
                for sj in failedsubjobs:
                    sj.reset()
            self.deliveryclerk.send_job(self, STORAGE)
            self.status
            self._update_job_in_database(True)
            STORAGE.flush()

    def cancelpreparation(self, **kwargs):
        for n in self.range_subjobs:
            if self.subjobs.get(n, None):
                del self.subjobs[n]
        self.jobtable.purge()
        self._status = "new"

    def remove(self):
        if self.jobnumber:
            info_msg = "INFO\tremoving job {0}".format(self.jobnumber)
        else:
            info_msg = "INFO\tremoving job"
        print(info_msg)

        if self.status != "new":
            sjkill = self.deliveryclerk.kill(job=self)

        if len(self.keys) > 0:

            for n in self.range_subjobs:
                sj = self[n]

                if sj and sj.status == "running":
                    sj.kill(storeparent=False, sjkill=sjkill)

        self.database.purge_table("job_{}".format(self.jobnumber))
        self.database.table("jobs").remove(doc_ids=[self.jobnumber])

    def __getitem__(self, sjob_number):

        if DEBUG > 0:
            msg = "in SimulationJob.__getitem__, jobnumber:{0}, sjobnumber={1}"
            print(msg.format(self.jobnumber, sjob_number))

        if not isinstance(sjob_number, int):
            msg = "Job number must be a 'int'. Got a '{0}' instead!"
            raise TypeError(msg.format(sjob_number.__class__.__name__))

        if len(self.keys) == 0:
            raise JobNotPreparedError("Please 'prepare' the job before doing this!")

        if sjob_number not in self.keys:
            print(
                "WARNING\tsubjob {0}.{1} has been lost!".format(
                    self.jobnumber, sjob_number
                )
            )
            self.subjobs[sjob_number] = self._load_subjob(sjob_number, force_load=True)

        subjob = self.subjobs[sjob_number]

        if subjob is None:
            self.subjobs[sjob_number] = self._load_subjob(sjob_number, force_load=True)

        return self.subjobs[sjob_number]

    def __setitem__(self, sjob_number, subjob):

        if not isinstance(sjob_number, int):
            msg = "Job number must be a 'int'. Got a '{0}' instead!"
            raise TypeError(msg.format(sjob_number.__class__.__name__))

        if subjob:
            if not isinstance(subjob, SimulationSubJob):
                msg = "Must receive a SimulationSubJob. Got a '{0}' instead!"
                raise TypeError(msg.format(subjob.__class__.__name__))

        self.subjobs[sjob_number] = subjob

    def __iter__(self):
        for n in self.range_subjobs:
            yield self[n]

    def select(self, status, update=True):
        if update:
            return [self[n] for n in self.range_subjobs if self[n].status == status]
        else:
            return [
                self[n] for n in self.range_subjobs if self[n].last_status == status
            ]

    @property
    def last_status(self):
        return self._status

    @property
    def status(self):

        if DEBUG > 0:
            print("in SimulationJob.status, jobnumber:{0}".format(self.jobnumber))

        if len(self.keys) == 0:
            return "new"

        if self.last_status == "prepared":
            self._update_job_in_database(True)

        if not self.last_status == "completed":

            nsubmitted = 0
            nrunning = 0
            ncompleted = 0
            nfailed = 0

            keys = self.keys

            for n in self.range_subjobs:

                if n in keys:
                    sj_doc = self.jobtable.get(doc_id=n)
                    subjob = self.subjobs[n]

                    if sj_doc is None:
                        status = "notfound"
                    elif subjob is None:
                        status = sj_doc["status"]
                    else:
                        status = subjob.status
                        jobid = subjob.jobid

                        _dict = {}

                        if sj_doc["jobid"] != jobid:
                            _dict["jobid"] = jobid
                        if sj_doc["status"] != status:
                            _dict["status"] = status

                        if len(_dict) > 0:
                            self.jobtable.update(_dict, doc_ids=[n])

                        if status in ["completed", "failed"]:
                            self[n] = None

                else:
                    status = "new"

                if status == "submitted":
                    nsubmitted += 1
                elif status == "running":
                    nrunning += 1
                    nsubmitted += 1
                elif status == "completed":
                    ncompleted += 1
                    nsubmitted += 1
                elif status == "failed":
                    nfailed += 1
                    nsubmitted += 1

            if nsubmitted == 0:
                _status = "prepared"
            elif nsubmitted < self.nsubjobs and nsubmitted > 0:
                _status = "submitting"
            elif (
                nsubmitted == self.nsubjobs
                and nrunning == 0
                and nfailed == 0
                and ncompleted < self.nsubjobs
            ):
                _status = "submitted"
            elif nsubmitted == self.nsubjobs and nrunning > 0:
                _status = "running"
            elif (
                nsubmitted == self.nsubjobs
                and nrunning == 0
                and ncompleted == self.nsubjobs
                and nfailed == 0
            ):
                _status = "completed"
            elif (
                nsubmitted == self.nsubjobs
                and nrunning == 0
                and ncompleted < self.nsubjobs
                and nfailed > 0
            ):
                if ncompleted + nfailed == self.nsubjobs:
                    _status = "failed"
                else:
                    _status = "submitted"

            if _status == "completed":
                self.deliveryclerk.clear(self)

            if _status != self._status:
                info_msg = "INFO\tstatus of job {0} changed from '{1}' to '{2}'"
                info_msg = info_msg.format(self.jobnumber, self._status, _status)

                print(info_msg)
                self._status = _status
                self._update_job_in_database(True)

            self._status = _status

        if DEBUG > 0:
            print("Out of SimulationJob.status, jobnumber:{0}".format(self.jobnumber))

        return self._status

    def _setoptfile(self):
        moddir = os.getenv("SIMPRODPATH")
        self._optfile = "{0}/EvtTypes/{1}/{1}.py".format(moddir, self._evttype)

        if not os.path.isfile(self._optfile):
            getevttype(evttype=self._evttype, decfiles=self.decfiles)

    def outdict(self):

        status = self.last_status

        outdict = {
            "evttype": self.evttype,
            "year": self.year,
            "nevents": self.nevents,
            "neventsjob": self.neventsjob,
            "nsubjobs": self.nsubjobs,
            "runnumber": self._runnumber,
            "simcond": self.simcond,
            "polarities": self.polarities,
            "stripping": self.stripping,
            "simmodel": self.simmodel,
            "mudst": self.mudst,
            "turbo": self.turbo,
            "basedir": self.options["basedir"],
            "proddir": self.proddir,
            "destdir": self.destdir,
            "subdir": self.options["subdir"],
            "loginprod": self.options["loginprod"],
            "screensessions": self.screensessions,
            "status": status,
            "keeplogs": self.keeplogs,
            "keepxmls": self.keepxmls,
            "redecay": self.redecay,
            "deliveryclerk": self.deliveryclerk.outdict(),
        }

        outdict["nrunning"] = 0
        outdict["ncompleted"] = 0
        outdict["nfailed"] = 0

        if outdict["status"] not in ["new", "prepared"]:
            try:
                outdict["nrunning"] = len(self.select("running", False))
                outdict["ncompleted"] = len(self.select("completed", False))
                outdict["nfailed"] = len(self.select("failed", False))
            except TypeError:
                pass

        if not self.options["loginprod"]:
            outdict["logdir"] = self.options["logdir"]
            outdict["logdestdir"] = self.options["logdestdir"]

        return outdict

    def _update_job_in_database(self, update_subjobs_in_database=False):

        if DEBUG > 0:
            print(
                "in SimulationJob._update_job_in_database, jobnumber:{0}".format(
                    self.jobnumber
                )
            )

        jobstable = self.database.table("jobs")

        jobstable.update(self.outdict(), doc_ids=[self.jobnumber])

        if update_subjobs_in_database:
            if DEBUG > 0:
                print("in SimulationJob._update_job_in_database, update subjobs")
            table = self.deliveryclerk.get_update_subjobs_in_database(self)

            for n in self.range_subjobs:

                job = self[n]

                if job.status in ["prepared", "new"] and isinstance(job.jobid, int):
                    job._status = Status("submitted", job.output)
                    continue

                if job._status.isvalid and not job.status == "submitted":
                    continue

                if job.status == "completed":
                    continue

                else:
                    if table is not None:
                        doc = table.get(Query().subjobnumber == n)
                        if DEBUG > 0:
                            print(n, doc)
                    else:
                        doc = None

                    if doc is not None:
                        if DEBUG > 0:
                            print(n, doc["runnumber"], self.getrunnumber(n))
                        assert doc["runnumber"] == self.getrunnumber(n)

                        if doc["jobid"] != job.jobid:
                            job.jobid = doc["jobid"]
                        if doc["status"] != job.status and job.status == "prepared":
                            job._status = Status(doc["status"], job.output)

                        if doc["status"] != "prepared" and doc["jobid"] is not None:
                            job._status.submitted = True

                    else:
                        job._update_subjob_in_database()

        if DEBUG > 0:
            print(
                "Out of SimulationJob._update_job_in_database, jobnumber:{0}".format(
                    self.jobnumber
                )
            )

    @classmethod
    def from_dict(cls, dict, jobnumber, inscreen=False, printlevel=1, **kwargs):

        if DEBUG > 1:
            print("in SimulationJob.from_dict")

        if not py3:
            for k in dict.keys():
                if isinstance(dict[k], unicode):
                    dict[k] = dict[k].encode("utf-8")

        simjob = cls(
            evttype=dict["evttype"],
            year=dict["year"],
            nevents=dict["nevents"],
            neventsjob=dict["neventsjob"],
            runnumber=dict["runnumber"],
            polarities=dict.get("polarities", None),
            simcond=dict["simcond"],
            stripping=dict["stripping"],
            simmodel=dict.get("simmodel", "pythia8"),
            mudst=dict["mudst"],
            turbo=dict["turbo"],
            basedir=dict["basedir"],
            newjob=False,
            jobnumber=jobnumber,
            **kwargs
        )

        simjob.jobnumber = jobnumber
        simjob._options["subdir"] = dict["subdir"]
        simjob._options["loginprod"] = dict["loginprod"]
        simjob.screensessions = dict["screensessions"]
        simjob._status = dict.get("status", "new")
        simjob._keeplogs = dict.get("keeplogs", True)
        simjob._keepxmls = dict.get("keepxmls", True)
        simjob._redecay = dict.get("redecay", False)

        if not simjob._options["loginprod"]:
            simjob._options["logdir"] = dict["logdir"]
            simjob._options["logdestdir"] = dict["logdestdir"]

        simjob._options["cpumemory"] = dict.get("cpumemory", None)
        if not simjob._options["cpumemory"]:
            simjob._options["cpumemory"] = dict.get("cpu", None)

        simjob.deliveryclerk = DeliveryClerk.from_dict(dict["deliveryclerk"], **kwargs)

        if DEBUG > 1:
            print(simjob.jobtable)

        if len(simjob.jobtable) > 0:

            if printlevel > 0:
                t = tqdm(
                    total=simjob.nsubjobs,
                    bar_format="{l_bar}%s{bar}%s{r_bar}" % (Fore.BLUE, Fore.RESET),
                    desc=cyan("\tLoading subjobs"),
                )
            else:
                t = None

            simjob.subjobs = {
                n: simjob._load_subjob(n, t, printlevel) for n in simjob.range_subjobs
            }

            if printlevel > 0:
                t.close()

        return simjob

    @classmethod
    def from_doc(cls, doc, inscreen=False, printlevel=1, **kwargs):

        if DEBUG > 1:
            print("in SimulationJob.from_doc")

        jobnumber = doc.doc_id
        simjob = cls.from_dict(doc, jobnumber, inscreen, printlevel, **kwargs)

        return simjob

    def _load_subjob(self, nsj, pbar=None, printlevel=0, force_load=False):

        sj_doc = self.jobtable.get(doc_id=nsj)

        if sj_doc is not None:
            status = sj_doc["status"]

            if status in ["completed", "failed"] and not force_load:
                sj = None
            else:
                sj = SimulationSubJob.from_doc(self, sj_doc)
        else:
            sj = None

        if printlevel > 0:
            pbar.update(1)

        return sj

    def __str__(self):

        if len(self.subjobs) > 0 and len(self.jobtable) > 0:

            toprint = []

            toprint.append(
                "evttype: {0}; year: {1}; #events {2}; stripping {3}; simcond {4}; {5} jobs".format(
                    self.evttype,
                    self.year,
                    self.nevents,
                    self.stripping,
                    self.simcond,
                    self.nsubjobs,
                )
            )

            h_job = "    #job "
            h_jobID = "    job ID "
            h_status = "       status "
            h_runnumber = "      runnumber "
            h_polarity = "   polarity "
            h_nevents = "  #events "

            header = [h_job, h_jobID, h_status, h_runnumber, h_polarity, h_nevents]
            header = "|".join(header) + "|"
            line = "".join(["-" for i in range(len(header) - 2)])

            toprint.append(line)
            toprint.append(header)
            toprint.append(line)

            for n in self.range_subjobs:

                sj_doc = self.jobtable.get(doc_id=n)

                if self.subjobs[n] is None:
                    status = sj_doc["status"]
                    jobID = sj_doc["jobid"]
                    runnumber = self.getrunnumber(n)
                    polarity = sj_doc["polarity"]
                else:
                    job = self[n]
                    status = job.status
                    jobID = job.jobid
                    runnumber = job.runnumber
                    polarity = job.polarity

                    _dict = {}

                    if sj_doc["jobid"] != job.jobid:
                        _dict["jobid"] = job.jobid
                    if sj_doc["status"] != job.status:
                        _dict["status"] = job.status

                    if len(_dict) > 0:
                        self.jobtable.update(_dict, doc_ids=[n])

                nevents = self.neventsjob

                if status == "submitted":
                    color = cyan
                elif status == "new":
                    color = cdefault
                elif status == "running":
                    color = green
                elif status == "completed":
                    color = blue
                elif status == "failed":
                    color = red

                p_job = "{n:{fill}{al}{w}} ".format(
                    w=(len(h_job) - 1), al=">", fill="", n=n
                )

                p_jobID = "{n:{fill}{al}{w}} ".format(
                    w=(len(h_jobID) - 1), al=">", fill="", n=jobID
                )

                p_status = "{n:{fill}{al}{w}} ".format(
                    w=(len(h_status) - 1), al=">", fill="", n=status
                )

                p_runnumber = "{n:{fill}{al}{w}} ".format(
                    w=(len(h_runnumber) - 1), al=">", fill="", n=runnumber
                )

                p_polarity = "{n:{fill}{al}{w}} ".format(
                    w=(len(h_polarity) - 1), al=">", fill="", n=polarity
                )

                p_nevents = "{n:{fill}{al}{w}} ".format(
                    w=(len(h_nevents) - 1), al=">", fill="", n=nevents
                )

                linejob = (
                    "|".join(
                        [p_job, p_jobID, p_status, p_runnumber, p_polarity, p_nevents]
                    )
                    + "|"
                )

                toprint.append(color(linejob))

            toprint = "\n".join(toprint)

        else:
            toprint = self.__repr__()

        return toprint

    def _repr_pretty_(self, p, cycle):
        if cycle:
            p.text("simulation job...")
            return
        p.text(self.__str__())


class SimulationSubJob(object):
    """
    Simulation subjob.
    """

    def __init__(self, parent, polarity, runnumber, subjobnumber, **kwargs):
        self.parent = parent
        self.polarity = polarity
        self.runnumber = runnumber
        self.subjobnumber = subjobnumber
        self.jobid = None
        self.send_options = self.parent.options.copy()
        self._infiles = kwargs.get("infiles", [])
        self.send_options["infiles"] = self._infiles
        self.keeplog = self.parent.keeplogs
        self.keepxml = self.parent.keepxmls

        self.jobname = "{0}_{1}_{2}evts_s{3}_{4}".format(
            self.parent.year,
            self.polarity,
            self.parent.neventsjob,
            self.parent.stripping,
            self.runnumber,
        )

        self.send_options["jobname"] = self.jobname

        self.jobdir = "{0}/{1}".format(self.parent.proddir, self.jobname)

        ext = "dst"
        if self.parent.mudst:
            ext = "mdst"

        self.prodfile = "{0}/{1}_events.{2}".format(
            self.jobdir, self.parent.neventsjob, ext
        )

        self.destfile = "{0}/{1}/{2}evts_s{3}_{4}.{5}".format(
            self.parent.destdir,
            self.polarity,
            self.parent.neventsjob,
            self.parent.stripping,
            self.runnumber,
            ext,
        )

        if not self.send_options["loginprod"]:
            self.logjobdir = "{0}/{1}".format(
                self.send_options["logdestdir"], self.jobname
            )

        self._status = Status(status="new", output=self.output)

        if kwargs.get("newsubjob", True):
            self.parenttable.insert(self.outdict())
            assert self.parenttable._last_id == subjobnumber

        if kwargs.get("to_store", False):
            self._update_subjob_in_database()

    @property
    def parenttable(self):
        return self.parent.jobtable

    @property
    def infiles(self):
        return self._infiles

    @infiles.setter
    def infiles(self, files):
        if not isinstance(files, (list, tuple)):
            raise TypeError("A list/tuple with infiles must me provided.")

        types = [str]
        if not py3:
            types.append(unicode)

        if not all(isinstance(f, types) for f in files):
            raise TypeError("Infiles must be str.")

        self._infiles = files
        self.send_options["infiles"] = files

    def send(self):

        if not self._status.submitted:

            self.jobid = self.parent.deliveryclerk.send_subjob(self)

            if self.jobid:
                self._status = Status("submitted", self.output)
                print(
                    blue(
                        "{0}/{1} jobs submitted!".format(
                            int(self.subjobnumber), self.parent.nsubjobs
                        )
                    )
                )
            else:
                print(
                    red(
                        "job {0}/{1} submission failed, try later!".format(
                            int(self.subjobnumber), self.parent.nsubjobs
                        )
                    )
                )

            self._update_subjob_in_database()

    @property
    def last_status(self):
        return self._status

    @property
    def status(self):
        if DEBUG > 0:
            print("in SimulationSubJob.status")

        previous_status = self.last_status

        if previous_status != "failed" and previous_status != "completed":
            if not self._status.finished and self._status.submitted:
                # update status
                if not self._status.isvalid:
                    status = self.parent.deliveryclerk.getstatus(self.jobid)
                    if status != "error":
                        self._status = Status(status, self.output)

            if previous_status != self._status:

                info_msg = "INFO\tstatus of subjob {0}.{1} changed from '{2}' to '{3}'"
                info_msg = info_msg.format(
                    self.parent.jobnumber,
                    self.subjobnumber,
                    previous_status,
                    self._status,
                )

                print(info_msg)
                self._update_subjob_in_database()

        if self._status.completed:
            if not self.output == self.destfile and not self.output == "":
                self._move_jobs()
        elif self._status.failed:
            self._empty_proddir(keep_log=True)

        return repr(self._status)

    @property
    def output(self):
        if os.path.isfile(self.prodfile):
            return self.prodfile
        elif os.path.isfile(self.destfile):
            return self.destfile
        else:
            return ""

    def reset(self):

        if self._status == "running":
            self.kill()

        self._empty_proddir()
        self.jobid = None
        self._status = Status("new", self.output)
        self._update_subjob_in_database()

    def command(self):
        command = dict(doprod=self.parent.doprod)
        command["args"] = []
        command["args"].append(self.parent.optfile)
        command["args"].append(self.parent.neventsjob)
        command["args"].append(self.polarity)
        command["args"].append(self.runnumber)
        command["args"].append(self.parent.turbo)
        command["args"].append(self.parent.mudst)
        command["args"].append(self.parent.stripping)
        command["args"].append(self.parent.redecay)
        command["args"].append(self.parent.simmodel)
        return command

    def kill(self, storeparent=True, sjkill=True):

        info_msg = "INFO\tkilling subjob {0}.{1}"
        info_msg = info_msg.format(self.parent.jobnumber, self.subjobnumber)
        print(info_msg)

        if sjkill:
            if self._status.submitted:
                self.parent.deliveryclerk.killsubjob(self.jobid)

        self._status = Status("failed", self.output)
        self._update_subjob_in_database()
        if storeparent:
            self.parent._update_job_in_database()
        self._empty_proddir()

    def _empty_proddir(self, keep_log=False):
        if os.path.isdir(self.jobdir):
            if keep_log and self.send_options["loginprod"]:
                files = glob.iglob(self.jobdir + "/*")
                for f in files:
                    if "out" in f:
                        continue
                    elif "err" in f:
                        continue
                    else:
                        os.remove(f)
            else:
                silentrm(self.jobdir)

        if not self.send_options["loginprod"] and not keep_log:
            if os.path.isdir(self.logjobdir):
                silentrm(self.logjobdir)

    def _move_jobs(self):

        if not os.path.isdir(self.jobdir):
            msg = (
                " WARNING: production folder has been removed, if the jobs is marked as"
            )
            msg += "failed the output hasbeen probably lost!"
            warnings.warn(red(msg), stacklevel=2)

        else:
            dst_prodfile = self.prodfile

            if "eos" in dst_prodfile:
                mover = EosMove
            else:
                mover = Move

            xml_prodfile = os.path.dirname(dst_prodfile) + "/GeneratorLog.xml"
            dst_destfile = self.destfile
            xml_destfile = os.path.dirname(self.destfile) + "/xml/{0}.xml".format(
                self.runnumber
            )

            info_msg = "INFO\tMoving output of subjob {0}.{1} to {2}!"
            info_msg = info_msg.format(
                self.parent.jobnumber, self.subjobnumber, dst_destfile
            )
            print(info_msg)

            if os.path.isfile(dst_prodfile):
                mover(dst_prodfile, dst_destfile)
            else:
                warn_msg = red(
                    "WARNING\tdst output is not found. It has probably been moved or erased manually"
                )
                print(warn_msg)

            if self.keepxml:

                info_msg = (
                    "INFO\tMoving generator informations of subjob {0}.{1} to {2}!"
                )
                info_msg = info_msg.format(
                    self.parent.jobnumber, self.subjobnumber, xml_destfile
                )
                print(info_msg)

                if os.path.isfile(xml_prodfile):
                    mover(xml_prodfile, xml_destfile)
                else:
                    warn_msg = red(
                        "WARNING\tGeneratorLog.xml is not found. It has probably been moved or erased manually"
                    )
                    print(warn_msg)

            self._empty_proddir(self.keeplog)

    def outdict(self):

        outdict = {
            "runnumber": self.runnumber,
            "polarity": self.polarity,
            "jobid": self.jobid,
            "status": repr(self._status),
            "infiles": self.infiles,
        }

        if DEBUG > 0:
            print("in SimulationSubJob.outdict")
            print(outdict)
            print()

        if not self.send_options["loginprod"]:
            outdict["logjobdir"] = self.logjobdir

        return outdict

    def _update_subjob_in_database(self):

        self.parenttable.update(self.outdict(), Query().runnumber == self.runnumber)

    @classmethod
    def from_dict(cls, parent, dict, subjobnumber, to_store=True):

        simsubjob = cls(
            parent=parent,
            polarity=dict["polarity"],
            runnumber=dict["runnumber"],
            subjobnumber=subjobnumber,
            newsubjob=False,
        )

        if DEBUG > 1:
            print("In SimulationSubJob.from_dict, subjob={0}.".format(subjobnumber))

        simsubjob.jobid = dict["jobid"]
        simsubjob.infiles = dict.get("infiles", [])
        simsubjob.send_options["infiles"] = dict.get("infiles", [])

        status = dict["status"]

        simsubjob._status = Status(status, simsubjob.output, in_init=True)

        if not simsubjob.send_options["loginprod"]:
            simsubjob.logjobdir = dict["logjobdir"]

        if to_store:
            simsubjob._update_subjob_in_database()

        return simsubjob

    @classmethod
    def from_doc(cls, parent, doc, to_store=True):

        subjobnumber = doc.doc_id
        simsubjob = cls.from_dict(parent, doc, subjobnumber, to_store)

        return simsubjob
