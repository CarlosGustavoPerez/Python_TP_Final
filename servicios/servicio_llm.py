from huggingface_hub import InferenceClient
from config import HF_TOKEN


class ServicioLLM:

    def __init__(self):
        self.client = InferenceClient(
            token=HF_TOKEN
        )

    def _consultar_modelo(self, prompt):

        respuesta = self.client.chat.completions.create(
            model="meta-llama/Llama-3.1-8B-Instruct",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=500
        )

        return respuesta.choices[0].message.content

    def generar_informe(self, contexto):

        prompt = f"""
        Actúa como un analista de datos senior.

        Vas a recibir un resumen generado con Pandas.

        NO inventes información.

        Utiliza únicamente los datos proporcionados.

        Genera:

        # Resumen Ejecutivo

        # Hallazgos Relevantes

        # Riesgos Detectados

        # Recomendaciones

        # Próximos Pasos

        Responde en español.

        {contexto}
        """

        return self._consultar_modelo(prompt)

    def responder_pregunta(self, contexto, pregunta):

        prompt = f"""
        Actúa como un analista de datos.

        Utiliza únicamente la información proporcionada.

        Contexto:

        {contexto}

        Pregunta:

        {pregunta}

        Responde en español.
        """

        return self._consultar_modelo(prompt)