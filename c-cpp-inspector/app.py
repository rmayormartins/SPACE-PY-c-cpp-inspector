import gradio as gr
from clang.cindex import Index, CursorKind, TypeKind
from collections import Counter
from typing import Dict, List
import os

class CPPSyntaxAnalyzer:
    """C/C++-Inspector: Análise sintática e recursos específicos de C/C++"""

    def __init__(self):
        self.index = Index.create()

    def analyze_syntax(self, code: str, filename: str) -> Dict[str, int]:
        """Analisa elementos sintáticos e estruturais do código"""
        results = Counter()

        try:
            with open(filename, 'w') as f:
                f.write(code)

            tu = self.index.parse(filename)
            
            def visit_node(node):
                # Tipos primitivos
                if node.kind == CursorKind.VAR_DECL:
                    if node.type.kind in [TypeKind.INT, TypeKind.FLOAT, TypeKind.DOUBLE, 
                                        TypeKind.CHAR_S, TypeKind.BOOL]:
                        results["Tipos Primitivos"] += 1

                # Ponteiros
                if node.type.kind == TypeKind.POINTER:
                    results["Ponteiros"] += 1
                    # Ponteiros para ponteiros (ponteiros múltiplos)
                    if node.type.get_pointee().kind == TypeKind.POINTER:
                        results["Ponteiros Múltiplos"] += 1

                # Structs
                if node.kind == CursorKind.STRUCT_DECL:
                    results["Structs"] += 1

                # Unions
                if node.kind == CursorKind.UNION_DECL:
                    results["Unions"] += 1

                # Enums
                if node.kind == CursorKind.ENUM_DECL:
                    results["Enums"] += 1

                # Typedef
                if node.kind == CursorKind.TYPEDEF_DECL:
                    results["Typedefs"] += 1

                # Arrays
                if node.type.kind == TypeKind.CONSTANTARRAY:
                    results["Arrays"] += 1

                # Variáveis e Constantes
                if node.kind == CursorKind.VAR_DECL:
                    results["Variáveis Declaradas"] += 1
                    if "const" in [token.spelling for token in node.get_tokens()]:
                        results["Constantes"] += 1

                # Estruturas de Controle
                if node.kind == CursorKind.IF_STMT:
                    results["If/Else"] += 1
                elif node.kind == CursorKind.SWITCH_STMT:
                    results["Switch/Case"] += 1
                elif node.kind == CursorKind.FOR_STMT:
                    results["For Loops"] += 1
                elif node.kind == CursorKind.WHILE_STMT:
                    results["While Loops"] += 1
                elif node.kind == CursorKind.DO_STMT:
                    results["Do-While Loops"] += 1

                # Entrada/Saída
                if node.kind == CursorKind.CALL_EXPR:
                    func_name = node.spelling.lower()
                    if func_name in ['printf', 'cout', 'puts', 'fprintf']:
                        results["Funções de Saída"] += 1
                    elif func_name in ['scanf', 'cin', 'gets', 'fscanf']:
                        results["Funções de Entrada"] += 1

                # Análise recursiva
                for child in node.get_children():
                    visit_node(child)

            visit_node(tu.cursor)

            # Análise de operadores e funções específicas via texto
            code_text = code.lower()
            
            # Operadores
            operators = {
                "Aritméticos": ["+", "-", "*", "/", "%"],
                "Comparação": ["==", "!=", ">", "<", ">=", "<="],
                "Lógicos": ["&&", "||", "!"],
                "Bit a Bit": ["&", "|", "^", "<<", ">>", "~"],
                "Atribuição": ["+=", "-=", "*=", "/=", "&=", "|=", ">>=", "<<="],
            }
            for category, ops in operators.items():
                results[category] = sum(code_text.count(op) for op in ops)

            # Gerenciamento de Memória
            memory_funcs = {
                "malloc": code_text.count("malloc("),
                "calloc": code_text.count("calloc("),
                "realloc": code_text.count("realloc("),
                "free": code_text.count("free("),
                "new": code_text.count("new "),
                "delete": code_text.count("delete "),
                "delete[]": code_text.count("delete[]"),
            }
            results["Alocação Dinâmica (malloc/new)"] = memory_funcs["malloc"] + memory_funcs["calloc"] + memory_funcs["new"]
            results["Liberação de Memória (free/delete)"] = memory_funcs["free"] + memory_funcs["delete"] + memory_funcs["delete[]"]
            results["Realocação (realloc)"] = memory_funcs["realloc"]

            # Manipulação de Memória
            memory_ops = {
                "memcpy": code_text.count("memcpy("),
                "memmove": code_text.count("memmove("),
                "memset": code_text.count("memset("),
                "memcmp": code_text.count("memcmp("),
            }
            results["Operações de Memória"] = sum(memory_ops.values())

        except Exception as e:
            results["Erro"] = str(e)

        return dict(results)

    def analyze_cpp_features(self, code: str, filename: str) -> Dict[str, int]:
        """Analisa recursos específicos de C++"""
        results = Counter()

        try:
            with open(filename, 'w') as f:
                f.write(code)

            tu = self.index.parse(filename)

            def visit_node(node):
                # Classes
                if node.kind == CursorKind.CLASS_DECL:
                    results["Classes"] += 1

                # Templates
                if node.kind == CursorKind.CLASS_TEMPLATE:
                    results["Templates"] += 1

                # Namespace
                if node.kind == CursorKind.NAMESPACE:
                    results["Namespaces"] += 1

                # Referências
                if node.type.kind == TypeKind.LVALUEREFERENCE:
                    results["Referências"] += 1

                # Métodos
                if node.kind == CursorKind.CXX_METHOD:
                    results["Métodos"] += 1
                    # Virtual
                    if "virtual" in [token.spelling for token in node.get_tokens()]:
                        results["Métodos Virtuais"] += 1

                # Sobrecarga de Operadores
                if node.kind == CursorKind.CXX_METHOD and node.spelling.startswith("operator"):
                    results["Sobrecarga de Operadores"] += 1

                # Membros e Encapsulamento
                if node.kind == CursorKind.FIELD_DECL:
                    results["Atributos"] += 1
                    if node.access_specifier.name == "PRIVATE":
                        results["Membros Private"] += 1
                    elif node.access_specifier.name == "PROTECTED":
                        results["Membros Protected"] += 1

                # Herança
                if node.kind == CursorKind.CXX_BASE_SPECIFIER:
                    results["Herança"] += 1

                # Análise recursiva
                for child in node.get_children():
                    visit_node(child)

            visit_node(tu.cursor)

            # Análise de recursos específicos via texto
            code_text = code.lower()
            
            # STL e Recursos Modernos
            stl_containers = ["vector", "list", "map", "set", "queue", "stack", "deque"]
            results["Uso de STL"] = sum(code_text.count(container) for container in stl_containers)
            
            modern_features = ["auto", "nullptr", "constexpr", "static_assert", "decltype"]
            results["Recursos C++ Moderno"] = sum(code_text.count(feature) for feature in modern_features)

        except Exception as e:
            results["Erro"] = str(e)

        return dict(results)

def process_files(files) -> List[Dict]:
    """Processa múltiplos arquivos"""
    analyzer = CPPSyntaxAnalyzer()
    file_results = []

    for file in files:
        with open(file.name, 'r', encoding='utf-8') as f:
            code = f.read()
            
        syntax_results = analyzer.analyze_syntax(code, file.name)
        cpp_results = analyzer.analyze_cpp_features(code, file.name)
        
        combined_results = {**syntax_results, **cpp_results}
        combined_results["Arquivo"] = file.name
        file_results.append(combined_results)

    return file_results
def analyze_files(files):
    """Analisa os arquivos e retorna os resultados separados por categoria"""
    if not files:
        return [], [], [], [], [], [], [], []
        
    results = process_files(files)
    
    # Separar resultados por categoria
    file_info = [[result["Arquivo"]] for result in results]
    
    basic_elements = [[
        result.get("Tipos Primitivos", 0),
        result.get("Constantes", 0),
        result.get("Variáveis Declaradas", 0)
    ] for result in results]
    
    pointers_structs = [[
        result.get("Ponteiros", 0),
        result.get("Ponteiros Múltiplos", 0),
        result.get("Arrays", 0),
        result.get("Structs", 0),
        result.get("Unions", 0),
        result.get("Enums", 0),
        result.get("Typedefs", 0)
    ] for result in results]
    
    flow_control = [[
        result.get("If/Else", 0),
        result.get("Switch/Case", 0),
        result.get("For Loops", 0),
        result.get("While Loops", 0),
        result.get("Do-While Loops", 0)
    ] for result in results]
    
    operators = [[
        result.get("Aritméticos", 0),
        result.get("Comparação", 0),
        result.get("Lógicos", 0),
        result.get("Bit a Bit", 0),
        result.get("Atribuição", 0)
    ] for result in results]
    
    io_ops = [[
        result.get("Funções de Entrada", 0),
        result.get("Funções de Saída", 0)
    ] for result in results]
    
    memory = [[
        result.get("Alocação Dinâmica (malloc/new)", 0),
        result.get("Liberação de Memória (free/delete)", 0),
        result.get("Realocação (realloc)", 0),
        result.get("Operações de Memória", 0)
    ] for result in results]
    
    cpp_features = [[
        result.get("Classes", 0),
        result.get("Templates", 0),
        result.get("Namespaces", 0),
        result.get("Referências", 0),
        result.get("Métodos", 0),
        result.get("Métodos Virtuais", 0),
        result.get("Sobrecarga de Operadores", 0),
        result.get("Membros Private", 0),
        result.get("Membros Protected", 0),
        result.get("Herança", 0),
        result.get("Uso de STL", 0),
        result.get("Recursos C++ Moderno", 0)
    ] for result in results]
    
    return (file_info, basic_elements, pointers_structs, flow_control, 
            operators, io_ops, memory, cpp_features)

# Interface Gradio
with gr.Blocks(title="C/Cpp-Inspector") as demo:
    gr.Markdown("# C/Cpp-Inspector: Code Analysis")
    gr.Markdown("""
    <p>Ramon Mayor Martins: <a href="https://rmayormartins.github.io/" target="_blank">Website</a> | <a href="https://huggingface.co/rmayormartins" target="_blank">Spaces</a> | <a href="https://github.com/rmayormartins" target="_blank">Github</a></p>
    """)
    gr.Markdown("Faça upload dos arquivos C/C++ para análise detalhada das estruturas e recursos da linguagem.")

    with gr.Column():
        file_input = gr.File(label="Arquivos C/C++", file_types=[".c", ".cpp", ".h", ".hpp"], file_count="multiple")
        analyze_button = gr.Button("Analisar Arquivos")
        
        gr.Markdown("## Resultados da Análise")
        
        with gr.Tabs():
            with gr.TabItem("📁 Informações do Arquivo"):
                output_file = gr.Dataframe(
                    label="Arquivo",
                    headers=["Arquivo"]
                )
            
            with gr.TabItem("#️⃣ Elementos Básicos"):
                output_basic = gr.Dataframe(
                    label="Elementos Básicos",
                    headers=["Tipos Primitivos", "Constantes", "Variáveis Declaradas"]
                )
            
            with gr.TabItem("*️⃣ Ponteiros e Estruturas"):
                output_pointers = gr.Dataframe(
                    label="Ponteiros e Estruturas",
                    headers=["Ponteiros", "Ponteiros Múltiplos", "Arrays", 
                            "Structs", "Unions", "Enums", "Typedefs"]
                )
            
            with gr.TabItem("🔄 Controle de Fluxo"):
                output_flow = gr.Dataframe(
                    label="Controle de Fluxo",
                    headers=["If/Else", "Switch/Case", "For Loops", "While Loops", "Do-While Loops"]
                )
            
            with gr.TabItem("🔣 Operadores"):
                output_operators = gr.Dataframe(
                    label="Operadores",
                    headers=["Aritméticos", "Comparação", "Lógicos", "Bit a Bit", "Atribuição"]
                )
            
            with gr.TabItem("↕️ Entrada/Saída"):
                output_io = gr.Dataframe(
                    label="Entrada/Saída",
                    headers=["Funções de Entrada", "Funções de Saída"]
                )
            
            with gr.TabItem("⏺️ Gerenciamento de Memória"):
                output_memory = gr.Dataframe(
                    label="Gerenciamento de Memória",
                    headers=["Alocação Dinâmica (malloc/new)", "Liberação de Memória (free/delete)",
                            "Realocação (realloc)", "Operações de Memória"]
                )
            
            with gr.TabItem("⏭️ Recursos C++"):
                output_cpp = gr.Dataframe(
                    label="Recursos C++",
                    headers=["Classes", "Templates", "Namespaces", "Referências",
                            "Métodos", "Métodos Virtuais", "Sobrecarga de Operadores",
                            "Membros Private", "Membros Protected", "Herança",
                            "Uso de STL", "Recursos C++ Moderno"]
                )

        analyze_button.click(
            fn=analyze_files,
            inputs=file_input,
            outputs=[output_file, output_basic, output_pointers, output_flow,
                    output_operators, output_io, output_memory, output_cpp]
        )

if __name__ == "__main__":
    demo.launch()