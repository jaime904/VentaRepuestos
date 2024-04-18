"use client";
import {useState} from "react";

function formuVenta ()
{
    const [marca, setMarca] = useState("");
    const [precio, setPrecio] = useState("");
    const [modelo, setModelo] = useState("");
    const [anio, setAnio] = useState("");

    const agregar = async (e) => {
        e.preventDefault();
        const repuesto = {
            marca: marca,
            precio: precio,
            modelo: modelo,
            anio: anio
        };
        
        const res = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/api/venta/`,{	
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(repuesto),
        })
        const data = await res.json();
        console.log(data);
    }

    return (
        <div className="bg-slate-200 p-7">
            <form onSubmit={ agregar }>
                <h1 className="text-black fobot-bold">Agregar Repuesto</h1>
                <label htmlFor="nombre">Marca</label>
                <input type="text" id="nombre" name="nombre" className="bg-slate-400 rounded-md p-2 mb-2 block"
                    onChange={(e) => setMarca(e.target.value)}/>
                <label htmlFor="precio">Precio</label>
                <input type="number" id="precio" name="precio" className="bg-slate-400 rounded-md p-2 mb-2 block" 
                    onChange={(e) => setPrecio(e.target.value)} />
                <label htmlFor="cantidad">Modelo</label>
                <input type="text" id="cantidad" name="cantidad" className="bg-slate-400 rounded-md p-2 mb-2 block" 
                     onChange={(e) => setModelo(e.target.value)}/>
                <label htmlFor="total">Año</label>
                <input type="number" id="total" name="total" className="bg-slate-400 rounded-md p-2 mb-2 block"
                     onChange={(e) => setAnio(e.target.value)}/>
                <button className="text-black " type="submit">Agregar</button>
            </form>
        </div>
    );
} export default formuVenta;