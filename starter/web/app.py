import json
import os
import urllib.error
import urllib.request

import streamlit as st


API_BASE_URL = os.getenv(
    "API_BASE_URL",
    "http://127.0.0.1:8000"
).rstrip("/")


def post_json(path: str, payload: dict) -> dict:
    body = json.dumps(payload).encode("utf-8")

    request = urllib.request.Request(
        f"{API_BASE_URL}{path}",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urllib.request.urlopen(request, timeout=8) as response:
        return json.loads(
            response.read().decode("utf-8")
        )


st.set_page_config(
    page_title="SentiKampus Starter",
    page_icon="🎓",
    layout="centered",
)

st.title("SentiKampus — Starter Web")
st.write("Analisis sentimen berdasarkan masukan mahasiswa.")

text = st.text_area(
    "Masukan mahasiswa",
    value="Pelayanan akademik sangat membantu",
)

week = st.selectbox(
    "Konteks pertemuan",
    options=list(range(1, 17)),
    index=3,
)

if st.button("Analisis Sentimen", type="primary"):

    if len(text.strip()) < 3:
        st.warning("Teks minimal tiga karakter.")

    else:
        try:
            result = post_json(
                "/api/v1/predict",
                {
                    "text": text.strip(),
                    "week": int(week),
                    "include_explanation": False,
                },
            )

            st.success(
                f"Hasil: {result['label'].upper()}"
            )

            st.write(
                f"Confidence: {result['score'] * 100:.1f}%"
            )

            st.json(result)

        except urllib.error.HTTPError as exc:
            st.error(
                f"API mengembalikan HTTP {exc.code}"
            )

            try:
                detail = exc.read().decode("utf-8")
                st.code(detail)
            except Exception:
                pass

        except urllib.error.URLError as exc:
            st.error(
                "Tidak dapat terhubung ke API. "
                "Pastikan backend sudah berjalan."
            )
            st.caption(str(exc.reason))

        except (KeyError, TypeError, ValueError) as exc:
            st.error(
                f"Format respons API tidak sesuai: {exc}"
            )

        except Exception as exc:
            st.error(f"Prediksi gagal: {exc}")