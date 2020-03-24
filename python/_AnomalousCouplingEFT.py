from HiggsAnalysis.CombinedLimit.PhysicsModel import *
from HiggsAnalysis.CombinedLimit.SMHiggsBuilder import SMHiggsBuilder
import ROOT, os

class AnaliticAnomalousCouplingEFT(PhysicsModel):

    "Float independently cross sections and branching ratios"
    def __init__(self):
        PhysicsModel.__init__(self) # not using 'super(x,self).__init__' since I don't understand it
        self.mHRange = []
        self.poiNames = []
        self.numOperators = 15

        # NB: alphabetically sorted, do not reshuffle
        self.Operators = [
             'cW',
             'cHbox',
             'cHDD',
             'cHW',
             'cHWB',
             'cHl1',
             'cHl3',
             'cHe',
             'cHq1',
             'cHq3',
             'cll1',
             'cqq1',
             'cqq11',
             'cqq3',
             'cqq31',
            ]

        self.numOperators = len(self.Operators)


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
        self.modelBuilder.doVar("r[1,-10,10]")
        self.poiNames = "r"


        for operator in range(0, self.numOperators):
          self.modelBuilder.doVar("k_" + str(self.Operators[operator]) + "[0,-200,200]")
          self.poiNames += ",k_" + str(self.Operators[operator])

        #
        # model: SM + k*linear + k**2 * quadratic
        #
        #   SM        = Asm**2
        #   linear    = Asm*Absm
        #   quadratic = Absm**2
        #
        #  ... and extended to more operators
        #
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

        for operator in range(0, self.numOperators):

          # linear term in each Wilson coefficient
          self.modelBuilder.factory_("expr::linear_func_"+ str(self.Operators[operator]) + "(\"@0*@1\",r,k_" + str(self.Operators[operator]) + ")")

          # quadratic term in each Wilson coefficient
          self.modelBuilder.factory_("expr::quadratic_func_"+ str(self.Operators[operator]) + "(\"@0*@1*@1\",r,k_" + str(self.Operators[operator]) + ")")

          # interference between pairs of Wilson coefficients
          for operator_sub in range(operator+1, self.numOperators):
            self.modelBuilder.factory_("expr::linear_func_mixed_" + str(self.Operators[operator]) + "_" + str(self.Operators[operator_sub]) +"(\"@0*@1*@2\",r,k_" + str(self.Operators[operator]) + ",k_" + str(self.Operators[operator_sub]) + ")")

        print " parameters of interest = ", self.poiNames
        self.modelBuilder.doSet("POI",self.poiNames)


#
# Define how the yields change
#


    def getYieldScale(self,bin,process):

        if   process == "SSWW":          return "sm_func"

        for operator in range(0, self.numOperators):
          if process == str(self.Operators[operator])+"_int" :    return "linear_func_"+ str(self.Operators[operator])
          if process == str(self.Operators[operator])+"_bsm" :    return "quadratic_func_"+ str(self.Operators[operator])
          for operator_sub in range(operator+1, self.numOperators):
            if (process == str(self.Operators[operator]) + "_" + str(self.Operators[operator_sub])) or (process == str(self.Operators[operator_sub]) + "_" + str(self.Operators[operator])):
              return "linear_func_mixed_" + str(self.Operators[operator]) + "_" + str(self.Operators[operator_sub])

        return 1



analiticAnomalousCouplingEFT = AnaliticAnomalousCouplingEFT()
