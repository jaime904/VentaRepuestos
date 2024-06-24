
export async function CargarVenta ()
{
    const res = await fetch(`${process.env.BACKEND_URL}/venta/`, {method: "GET"});
    const data = await res.json();
    console.log(data);
    return data;
}

export async function ListarVenta () //comentario de prueba3
{
    const date = await CargarVenta();
    console.log(date);
    return (
        <div className="bg-slate-700 px-4 w-full" >
            <h2>lista de RepuestoDisponibles</h2>
            {date.map(venta => (
                <div key={venta.id} className="bg-slate-500 px-4 py-3 mb-2">
                    <p>Marca: {venta.marca}</p>
                    <p>Precio: {venta.precio}</p>
                    <p>Modelo: {venta.modelo}</p>
                    <p>Año: {venta.anio}</p>
                    <div className="flex justify-between gap-x-2">
                        <button className="bg-blue-500 rounded-md p-2">Editar</button>
                        <button className="bg-red-500 text-white rounded-md p-2">Eliminar</button>
                    </div>
                </div>
            ))}

        </div>
    );
} export default ListarVenta;