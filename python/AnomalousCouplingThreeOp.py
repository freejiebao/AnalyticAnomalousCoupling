#text2workspace.py        datacard_0p3_ptj2.txt     -P HiggsAnalysis.AnalyticAnomalousCoupling.AnomalousCouplingTwoOp:analiticAnomalousCouplingTwoOp                 --PO=k_my_1,k_my_2,r  -o      data_0p3_ptj2.root

from HiggsAnalysis.CombinedLimit.PhysicsModel import *
from HiggsAnalysis.CombinedLimit.SMHiggsBuilder import SMHiggsBuilder
import ROOT, os

class AnaliticAnomalousCouplingThreeOp(PhysicsModel):

#
# standard, not touched
#

    "Float independently cross sections and branching ratios"
    def __init__(self):
        PhysicsModel.__init__(self) # not using 'super(x,self).__init__' since I don't understand it
        self.mHRange = []
        self.poiNames = []

    def setPhysicsOptions(self,physOptions):
        for po in physOptions:
            if po.startswith("higgsMassRange="):
                self.mHRange = po.replace("higgsMassRange=","").split(",")
                if len(self.mHRange) != 2:
                    raise RuntimeError, "Higgs mass range definition requires two extrema"
                elif float(self.mHRange[0]) >= float(self.mHRange[1]):
                    raise RuntimeError, "Extrema for Higgs mass range defined with inverterd order. Second must be larger the first"

#
# standard, not touched (end)
#


#
# Define parameters of interest
#

    def doParametersOfInterest(self):
        """Create POI and other parameters, and define the POI set."""

        # trilinear Higgs couplings modified
        self.modelBuilder.doVar("k_my_1[1,-200,200]")
        self.poiNames = "k_my_1"
        self.modelBuilder.doVar("k_my_2[1,-200,200]")
        self.poiNames += ",k_my_2"
        self.modelBuilder.doVar("k_my_3[1,-200,200]")
        self.poiNames += ",k_my_3"
        self.modelBuilder.doVar("r[1,-10,10]")
        self.poiNames += ",r"

        #
        # model: SM + k*linear + k**2 * quadratic
        #
        #   SM        = Asm**2
        #   linear_1        = Asm*Abs_1
        #   linear_2        = Asm*Absm_2
        #   linear_3        = Absm_1*Absm_2
        #   quadratic_1 = Absm_1**2
        #   quadratic_2 = Absm_2**2
        #
        self.modelBuilder.factory_("expr::sm_func(\"@0\",r)")
        self.modelBuilder.factory_("expr::linear_func_1(\"@0*@1\",r,k_my_1)")
        self.modelBuilder.factory_("expr::linear_func_2(\"@0*@1\",r,k_my_2)")
        self.modelBuilder.factory_("expr::linear_func_3(\"@0*@1\",r,k_my_3)")
        self.modelBuilder.factory_("expr::quadratic_func_1(\"@0*@1*@1\",r,k_my_1)")
        self.modelBuilder.factory_("expr::quadratic_func_2(\"@0*@1*@1\",r,k_my_2)")
        self.modelBuilder.factory_("expr::quadratic_func_3(\"@0*@1*@1\",r,k_my_3)")
        self.modelBuilder.factory_("expr::cross_func_1(\"@0*@1*@2\",r,k_my_1,k_my_2)")
        self.modelBuilder.factory_("expr::cross_func_2(\"@0*@1*@2\",r,k_my_1,k_my_3)")
        self.modelBuilder.factory_("expr::cross_func_3(\"@0*@1*@2\",r,k_my_2,k_my_3)")

        print self.poiNames
        self.modelBuilder.doSet("POI",self.poiNames)


#
# Define how the yields change
#


    def getYieldScale(self,bin,process):


        if process == "SSWW":          return "sm_func"
        elif process == "cW_int":    return "linear_func_1"
        elif process == "cHbox_int":    return "linear_func_2"
        elif process == "cHW_int":    return "linear_func_3"
        elif process == "cW_bsm": return "quadratic_func_1"
        elif process == "cHbox_bsm": return "quadratic_func_2"
        elif process == "cHW_bsm": return "quadratic_func_3"
        elif process == "cW_cHbox": return "cross_func_1"
        elif process == "cW_cHW": return "cross_func_2"
        elif process == "cHbox_cHW": return "cross_func_3"

        else:
          return 1



analiticAnomalousCouplingThreeOp = AnaliticAnomalousCouplingThreeOp()
