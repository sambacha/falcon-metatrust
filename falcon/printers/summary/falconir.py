"""
    Module printing summary of the contract
"""
from falcon.core.declarations import Function
from falcon.printers.abstract_printer import AbstractPrinter


def _print_function(function: Function) -> str:
    txt = ""
    for node in function.nodes:
        if node.expression:
            txt += f"\t\tExpression: {node.expression}\n"
            txt += "\t\tIRs:\n"
            for ir in node.irs:
                txt += f"\t\t\t{ir}\n"
        elif node.irs:
            txt += "\t\tIRs:\n"
            for ir in node.irs:
                txt += f"\t\t\t{ir}\n"
    return txt


class PrinterFalconIR(AbstractPrinter):
    ARGUMENT = "ir"
    HELP = "Print the falconIR representation of the functions"

    WIKI = " "

    def output(self, _filename):
        """
        _filename is not used
        Args:
            _filename(string)
        """

        txt = ""
        for compilation_unit in self.falcon.compilation_units:
            for contract in compilation_unit.contracts:
                if contract.is_top_level:
                    continue
                txt += f"Contract {contract.name}\n"
                for function in contract.functions:
                    txt += f'\tFunction {function.canonical_name} {"" if function.is_shadowed else "(*)"}\n'
                    txt += _print_function(function)
                for modifier in contract.modifiers:
                    txt += f"\tModifier {modifier.canonical_name}\n"
                    txt += _print_function(modifier)
            if compilation_unit.functions_top_level:
                txt += "Top level functions"
            for function in compilation_unit.functions_top_level:
                txt += f"\tFunction {function.canonical_name}\n"
                txt += _print_function(function)
        self.info(txt)
        res = self.generate_output(txt)
        return res
