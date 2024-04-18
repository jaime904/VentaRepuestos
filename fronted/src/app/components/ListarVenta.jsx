
async function CargarVenta ()
{
    const res = await fetch(`${process.env.BACKEND_URL}/api/venta/`);
    const data = await res.json();
    return data;
}

async function ListarVenta ()
{
    const date = await CargarVenta();
    console.log(date);
    return (
        <div className="bg-slate-700 p-4 w-full" >
            <h2>lista de RepuestoDisponibles</h2>
            {date.map((venta) => (
                <div key={venta._id} className="bg-slate-400 p-2 rounded-md m-2">
                    <h3>Marca: {venta.marca}</h3>
                    <p>Precio: {venta.precio}</p>
                    <p>Modelo: {venta.modelo}</p>
                    <p>Año: {venta.anio}</p>
                </div>
            ))}
        </div>
    );
} export default ListarVenta;