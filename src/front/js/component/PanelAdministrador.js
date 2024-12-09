import React from "react";
import { Sidebar } from "./Sidebar";
import { Outlet } from "react-router-dom";
import Administrador from "../../img/Administrador.png";

export const PanelAdministrador = () => {
  return (
    <div className="d-flex flex-column" style={{ height: "100%" }}>

      <div
        className="bg-dark text-white py-3 px-4 d-flex align-items-center justify-content-between"
        style={{
          width: "100%",
          height: "150px"
        }}
      >
        <div>
          <h1 className="mb-1">Panel de administrador</h1>
          <p className="mb-0">
            Funcionalidades para aprobar funcionarios/as,
            gestión del salón para los eventos y reserva o préstamo de libros.
          </p>
        </div>
        {/* Imagen banner */}
        <img
          src={Administrador}
          alt="Decoración"
          style={{
            height: "150px", 
            objectFit: "contain",
          }}
        />
      </div>

      {/* Contenido principal */}
      <div className="d-flex flex-grow-1">
        <Sidebar />
        <div className="flex-grow-1 p-3">
          <Outlet />
        </div>
      </div>
    </div>
  );
};
