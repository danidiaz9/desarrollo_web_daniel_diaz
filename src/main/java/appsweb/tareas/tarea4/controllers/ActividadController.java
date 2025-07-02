package appsweb.tareas.tarea4.controllers;

import appsweb.tareas.tarea4.models.Actividad;
import appsweb.tareas.tarea4.services.ActividadService;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.*;
import org.springframework.ui.Model;

import java.util.*;

@Controller
public class ActividadController {

    private final ActividadService actividadService;

    public ActividadController(ActividadService actividadService) {
        this.actividadService = actividadService;
    }

    // Vista de actividades finalizadas con su promedio
    @GetMapping("/evaluar")
    public String verListado(Model model) {
        Map<Actividad, Double> actividadesPromedio = actividadService.getCompletedActivitiesWithPromedio();
        model.addAttribute("actividadesPromedio", actividadesPromedio);
        return "evaluar-actividades";
    }

    // API para agregar una nota a una actividad (AJAX)
    @PostMapping("/api/actividad/{id}/nota")
    public ResponseEntity<Map<String, Object>> agregarNota(
            @PathVariable Integer id,
            @RequestBody Map<String, Object> body) {

        Object valorObj = body.get("valor");
        Integer valor = null;
        if (valorObj instanceof Number) {
            valor = ((Number) valorObj).intValue();
        } else if (valorObj instanceof String) {
            try {
                valor = Integer.parseInt((String) valorObj);
            } catch (NumberFormatException ignored) {}
        }

        if (valor == null || valor < 1 || valor > 7) {
            return ResponseEntity.badRequest()
                    .body(Map.of("error", "La nota debe estar entre 1 y 7"));
        }

        try {
            actividadService.agregarNotaActividad(id, valor);
            Double promedio = actividadService.getCompletedActivitiesWithPromedio()
                    .entrySet().stream()
                    .filter(e -> e.getKey().getId().equals(id))
                    .map(Map.Entry::getValue)
                    .findFirst()
                    .orElse(null);

            return ResponseEntity.ok(Map.of(
                    "id", id,
                    "nuevaNota", valor,
                    "promedio", promedio
            ));
        } catch (Exception e) {
            return ResponseEntity.status(404).body(Map.of("error", "Actividad no encontrada"));
        }
    }

    // API para obtener actividades finalizadas
    @GetMapping("/api/actividades/finalizadas")
    @ResponseBody
    public List<Map<String, Object>> actividadesFinalizadas() {
        Map<Actividad, Double> actividadesPromedio = actividadService.getCompletedActivitiesWithPromedio();
        List<Map<String, Object>> resultado = new ArrayList<>();
        for (Map.Entry<Actividad, Double> entry : actividadesPromedio.entrySet()) {
            Actividad act = entry.getKey();
            Double promedio = entry.getValue();
            Map<String, Object> map = new HashMap<>();
            map.put("id", act.getId());
            map.put("diaHoraInicio", act.getDiaHoraInicio());
            map.put("sector", act.getSector());
            map.put("nombre", act.getNombre());

            List<Map<String, Object>> temas = new ArrayList<>();
            if (act.getTemas() != null) {
                act.getTemas().forEach(t -> {
                    Map<String, Object> temaMap = new HashMap<>();
                    temaMap.put("tema", t.getTema() != null ? t.getTema().toString() : null);
                    temaMap.put("glosaOtro", t.getGlosaOtro());
                    temas.add(temaMap);
                });
            }
            map.put("temas", temas);

            map.put("promedioNotas", promedio);
            resultado.add(map);
        }
        return resultado;
    }

    @GetMapping("/")
    public String home() {
        return "redirect:/evaluar";
    }
}
