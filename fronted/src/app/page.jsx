import ListarVenta from "./components/ListarVenta";
import FormVenta from "./components/formVenta";

export const  dynamic = "force-dynamic"


function HomePage ()
{
    return (
        <div>
            <h2>Pagina Agregar Repuestos</h2>
            <div className="flex gap-x-10">
                <FormVenta />
                <ListarVenta />
            </div>
        </div>
    );
} export default HomePage;