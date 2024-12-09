import React from "react";
import { BrowserRouter, Route, Routes, Navigate } from "react-router-dom";
import ScrollToTop from "./component/scrollToTop";
import { BackendURL } from "./component/backendURL";


import { Home } from "./pages/home";
import { TuPerfil } from "./pages/TuPerfil";
import { EditarCargarLibro } from "./pages/EditarCargarLibro";
import { SubirLibro } from "./pages/SubirLibro";
import { PanelAdministrador } from "./component/PanelAdministrador";
import { EditarCargarSalon } from "./pages/EditarCargarSalon";
import { AdministradorUsuarios } from "./pages/AdministradorUsuarios";
import { Demo } from "./pages/demo";
import { Single } from "./pages/single";
import injectContext from "./store/appContext";

import { Navbar } from "./component/navbar";
//import { Footer } from "./component/footer";

const Layout = () => {
    const basename = process.env.BASENAME || "";
    const role = "admin";

    if (!process.env.BACKEND_URL || process.env.BACKEND_URL === "") return <BackendURL />;

    return (
        <div className="d-flex flex-column h-100">
            <BrowserRouter basename={basename}>
                <ScrollToTop>
                    <Navbar />
    
                    <div className="d-flex flex-grow-1">
                        <div className="flex-grow-1 p-0">
                            <Routes>
                                {/* Redirige automáticamente de "/" a "/perfil_administrador" */}
                                <Route path="/" element={<Navigate to="/panel_admin/perfil_administrador" replace />} />                   
                                <Route element={<PanelAdministrador />} path="/panel_admin">
                                <Route index element={<Navigate to="perfil_administrador" />} />
                                <Route element={<TuPerfil />} path="perfil_administrador" />
                                <Route element={<EditarCargarLibro />} path="editar_cargar_libro" />
                                <Route element={<SubirLibro />} path="subir_libro" />
                                <Route element={<EditarCargarSalon />} path="editar_cargar_salon" />
                                <Route element={<AdministradorUsuarios />} path="administrador_usuarios" />
                                </Route>
                                <Route element={<Home />} path="/" />
                                <Route element={<Demo />} path="/demo" />
                                <Route element={<Single />} path="/single/:theid" />
                                <Route element={<h1>Not found!</h1>} />
                            </Routes>
                        </div>
                    </div>
                </ScrollToTop>
            </BrowserRouter>
        </div>
    );
};

export default injectContext(Layout);



