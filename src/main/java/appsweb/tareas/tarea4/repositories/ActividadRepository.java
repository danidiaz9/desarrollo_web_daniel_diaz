package appsweb.tareas.tarea4.repositories;

import java.time.LocalDateTime;
import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import appsweb.tareas.tarea4.models.Actividad;

@Repository
public interface ActividadRepository extends JpaRepository<Actividad, Integer> {
    List<Actividad> findByDiaHoraTerminoBefore(LocalDateTime now);
}
