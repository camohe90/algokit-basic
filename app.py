from beaker import *
from pyteal import *


class MiEstado:
    total = GlobalStateValue(TealType.uint64)
    edad = GlobalStateValue(TealType.uint64)
        
app = (
    Application("Calculator", state=MiEstado())
    .apply(unconditional_create_approval, initialize_global_state=True)
    #.apply(unconditional_opt_in_approval, initialize_local_state=True)
)

@app.external
def hello(name: abi.String, *, output: abi.String) -> Expr:
    return output.set(Concat(Bytes("Hello, "), name.get()))

@app.external
def suma (numero1: abi.Uint64, numero2: abi.Uint64, *, output: abi.Uint64) -> Expr:
    return Seq(
        output.set(numero1.get()+ numero2.get()),
        app.state.total.set(numero1.get()+ numero2.get())
    )

@app.external
def resta (numero1: abi.Uint64, numero2: abi.Uint64, *, output: abi.Uint64) -> Expr:
    return Seq(
        output.set(numero1.get()+ numero2.get()),
        app.state.total.set(numero1.get() - numero2.get())
    )

@app.external
def multiplicacion (numero1: abi.Uint64, numero2: abi.Uint64, *, output: abi.Uint64) -> Expr:
    return Seq(
        output.set(numero1.get()+ numero2.get()),
        app.state.total.set(numero1.get() * numero2.get())
    )

@app.external
def division (numero1: abi.Uint64, numero2: abi.Uint64, *, output: abi.Uint64) -> Expr:
     return Seq(
        Assert(
            numero2.get() >= Int(1),
        ),
        output.set(numero1.get()/ numero2.get()),
        app.state.total.set(numero1.get() / numero2.get())
    )

@app.external
def validar_Edad(edad: abi.Uint64, *, output: abi.String) -> Expr:
    return (
        Cond(
        [ edad.get()>=Int(18),
            Seq(
                app.state.edad.set(edad.get()),
                output.set(Bytes("Ingreso permitido"))
            )
        ],
        [ edad.get()<Int(18),
            Seq(
                app.state.edad.set(edad.get()),
                output.set(Bytes("Ingreso no permitido"))
            )
        ]
        )
    )

@app.external
def validar_Edad_If(edad: abi.Uint64, *, output: abi.String) -> Expr:
    return (
        If(
            edad.get()>=Int(18),
            Seq(
                app.state.edad.set(edad.get()),
                output.set(Bytes("Ingreso permitido"))
            ), 
            Seq(
                app.state.edad.set(edad.get()),
                output.set(Bytes("Ingreso no permitido"))
            )
        )
    )

@app.external
def leer_Edad(*, output: abi.Uint64) -> Expr:
    return output.set(app.state.edad.get())

@app.external
def leer_resultado(*,output:abi.Uint64) -> Expr:
    return  output.set(app.state.total.get())

if __name__ == "__main__":
    app.build().export("./artifacts")
