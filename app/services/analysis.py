import logging
from typing import Dict, Any, Optional
from app.utils.logger import analysis_logger
from app.models.analysis import SyntacticProphet  # Asumiendo modelo existente
from app.schemas.hyperstition import FullAnalysisOutput  # Esquema de respuesta

class CognitiveIntegrator:
    def __init__(self):
        self.cognitive_weights = {
            'semantic': 0.4,
            'syntactic': 0.3,
            'network': 0.2,
            'psychoaffective': 0.1
        }

    def fuse_layers(self, 
                   hyperstition_data: Dict,
                   syntactic_data: Dict,
                   network_data: Dict) -> FullAnalysisOutput:
        """Integra múltiples capas analíticas en una estructura cognitiva unificada"""
        
        # 1. Validación de datos entrantes
        self._validate_inputs(hyperstition_data, syntactic_data, network_data)
        
        # 2. Cálculo de métricas combinadas
        cognitive_score = self._calculate_cognitive_index(
            hyperstition_data.get('semantic_score', 0),
            syntactic_data.get('complexity_score', 0),
            network_data.get('amplification_risk', 0)
        )
        
        # 3. Construcción de la respuesta unificada
        return FullAnalysisOutput(
            hyperstition=hyperstition_data,
            syntax=syntactic_data,
            network=network_data,
            cognitive_profile={
                "score": cognitive_score,
                "risk_category": self._classify_risk(cognitive_score)
            },
            discourse_style=self._detect_discourse_style(
                syntactic_data, 
                hyperstition_data
            )
        )

    def _calculate_cognitive_index(self, 
                                  semantic: float, 
                                  syntactic: float, 
                                  network: float) -> float:
        """Calcula índice cognitivo ponderado"""
        return round(
            (semantic * self.cognitive_weights['semantic']) +
            (syntactic * self.cognitive_weights['syntactic']) +
            (network * self.cognitive_weights['network']), 2
        )

class HyperstitionAnalyzer:
    def __init__(self, text: str):
        self.text = text
        self.integrator = CognitiveIntegrator()
        self.syntactic_engine = SyntacticProphet()
        self.analysis = {
            "base_layers": {},
            "cognitive_layer": {},
            "integrated_output": None
        }

    def _analyze_syntax(self) -> Dict:
        """Ejecuta análisis sintáctico completo"""
        return self.syntactic_engine.full_analysis(self.text)

    def full_analysis(self) -> FullAnalysisOutput:
        """Flujo completo de análisis integrado"""
        try:
            # Capa hipersticiosa
            self.analyze_semantic_layer()
            self.analyze_psychoaffective_layer()
            
            # Capa de red
            network_data = self.analyze_network_layer()
            
            # Capa sintáctica
            syntactic_data = self._analyze_syntax()
            
            # Integración cognitiva
            self.analysis["integrated_output"] = self.integrator.fuse_layers(
                hyperstition_data=self.analysis["base_layers"],
                syntactic_data=syntactic_data,
                network_data=network_data
            )
            
            return self.analysis["integrated_output"]

        except Exception as e:
            analysis_logger.error(f"Error de integración cognitiva: {str(e)}")
            raise

# ... (Mantener métodos existentes de HyperstitionAnalyzer sin cambios) ... 