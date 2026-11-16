"""Central configuration for the Dobot MG400 RAG chatbot."""
from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]  # project root
CHATBOT_DIR = Path(__file__).resolve().parents[1]

load_dotenv(CHATBOT_DIR / ".env")

# Paths
CORPUS_RAW = ROOT / "corpus" / "raw"
PROCESSED_DIR = CHATBOT_DIR / "data" / "processed"
CHROMA_DIR = CHATBOT_DIR / "data" / "chroma"
PROMPTS_DIR = CHATBOT_DIR / "prompts"
MANIFEST_PATH = PROCESSED_DIR / "manifest.jsonl"
CHUNKS_PATH = PROCESSED_DIR / "chunks.jsonl"

# Chroma
COLLECTION_NAME = os.getenv("CHROMA_COLLECTION", "mg400_full")

# Embeddings (local, no API key)
# Default: Qwen3-Embedding-0.6B — strong multilingual retrieval for RAG
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "Qwen/Qwen3-Embedding-0.6B")

# Ollama LLM (default: Qwen3.5-9B — fast + strong on RTX 5070 Ti 16GB)
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen3.5:9b")
OLLAMA_TIMEOUT = float(os.getenv("OLLAMA_TIMEOUT", "300"))
OLLAMA_TEMPERATURE = float(os.getenv("OLLAMA_TEMPERATURE", "0.2"))
# Qwen3 "thinking" is useful for hard reasoning but hurts RAG latency
OLLAMA_THINK = os.getenv("OLLAMA_THINK", "false").strip().lower() in {
    "1",
    "true",
    "yes",
    "on",
}

# Suggested models shown first in the UI (must still be installed in Ollama)
# Format: comma-separated tags, e.g. "qwen3.5:9b,qwen3:14b,llama3.2"
_RECOMMENDED_RAW = os.getenv(
    "OLLAMA_RECOMMENDED_MODELS",
    "qwen3.5:9b,qwen3:14b,llama3.2",
)
OLLAMA_RECOMMENDED_MODELS: list[str] = [
    m.strip() for m in _RECOMMENDED_RAW.split(",") if m.strip()
]

# Retrieval
TOP_K = int(os.getenv("TOP_K", "6"))
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "900"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "150"))

# Safety
SAFETY_PROMPT_PATH = PROMPTS_DIR / "system_prompt.txt"

# Curated text docs live under chatbot/data/curated
CURATED_DIR = CHATBOT_DIR / "data" / "curated"

# ---------------------------------------------------------------------------
# Explicit high-value sources (always included)
# path is relative to CORPUS_RAW, or "curated:filename.md" for curated files
# ---------------------------------------------------------------------------
CORE_SOURCES: list[dict] = [
    # --- Manuals ---
    {
        "path": "01_official_manuals/official_mg400_manual_user-guide_v1.7_20231116_en.pdf",
        "doc_type": "manual",
        "doc_title": "Dobot MG400 User Guide V1.7",
        "doc_version": "V1.7",
        "publish_date": "2023-11-16",
        "language": "en",
        "robot_model": "mg400",
        "axis_family": "4-axis",
        "applicability": "direct_mg400",
        "priority": "high",
        "safety_level": "warning",
        "source_type": "official_manual",
    },
    {
        "path": "01_official_manuals/official_mg400_datasheet_parameter-document_2022-07-28_en.pdf",
        "doc_type": "datasheet",
        "doc_title": "MG400 Parameter Document",
        "doc_version": "2022-07-28",
        "publish_date": "2022-07-28",
        "language": "en",
        "robot_model": "mg400",
        "axis_family": "4-axis",
        "applicability": "direct_mg400",
        "priority": "high",
        "safety_level": "caution",
        "source_type": "official_manual",
    },
    {
        "path": "01_official_manuals/official_mg400_m1pro_manual_dobotstudio-pro-user-guide_v2.8.0_20240226_en.pdf",
        "doc_type": "software_manual",
        "doc_title": "DobotStudio Pro User Guide V2.8.0 (MG400 & M1 Pro)",
        "doc_version": "V2.8.0",
        "publish_date": "2024-02-26",
        "language": "en",
        "robot_model": "mg400",
        "axis_family": "4-axis",
        "applicability": "mg400_m1pro",
        "priority": "high",
        "safety_level": "caution",
        "source_type": "official_manual",
    },
    {
        "path": "01_official_manuals/official_mg400_m1pro_manual_crstudio-user-guide_v4.13.0_2.14.0_20240311_en.pdf",
        "doc_type": "software_manual",
        "doc_title": "CRStudio User Guide V4.13.0 / 2.14.0 (MG400 & M1 Pro)",
        "doc_version": "V4.13.0_2.14.0",
        "publish_date": "2024-03-11",
        "language": "en",
        "robot_model": "mg400",
        "axis_family": "4-axis",
        "applicability": "mg400_m1pro",
        "priority": "high",
        "safety_level": "caution",
        "source_type": "official_manual",
    },
    # --- TCP/IP API (EN only; CN skipped as duplicate content) ---
    {
        "path": "02_api_sdk/official_mg400_api_tcp-ip-protocol-4axis_repo/TCP_IP Remote Control Interface Guide (4axis)_20240419_en.pdf",
        "doc_type": "api_reference",
        "doc_title": "TCP/IP Remote Control Interface Guide (4-axis)",
        "doc_version": "20240419",
        "publish_date": "2024-04-19",
        "language": "en",
        "robot_model": "mg400",
        "axis_family": "4-axis",
        "applicability": "mg400_m1pro",
        "priority": "high",
        "safety_level": "critical",
        "source_type": "official_github",
        "code_related": True,
    },
    # --- Python SDK ---
    {
        "path": "02_api_sdk/official_mg400_code_tcp-ip-4axis-python_repo/README-EN.md",
        "doc_type": "sdk_code",
        "doc_title": "TCP-IP-4Axis-Python README (EN)",
        "doc_version": "github",
        "publish_date": "unknown",
        "language": "en",
        "robot_model": "mg400",
        "axis_family": "4-axis",
        "applicability": "mg400_m1pro",
        "priority": "high",
        "safety_level": "caution",
        "source_type": "official_github",
        "code_related": True,
    },
    {
        "path": "02_api_sdk/official_mg400_code_tcp-ip-4axis-python_repo/dobot_api.py",
        "doc_type": "sdk_code",
        "doc_title": "dobot_api.py (TCP/IP 4-axis Python SDK)",
        "doc_version": "github",
        "publish_date": "unknown",
        "language": "en",
        "robot_model": "mg400",
        "axis_family": "4-axis",
        "applicability": "mg400_m1pro",
        "priority": "high",
        "safety_level": "critical",
        "source_type": "official_github",
        "code_related": True,
    },
    {
        "path": "02_api_sdk/official_mg400_code_tcp-ip-4axis-python_repo/PythonExample.py",
        "doc_type": "sdk_code",
        "doc_title": "PythonExample.py",
        "doc_version": "github",
        "publish_date": "unknown",
        "language": "en",
        "robot_model": "mg400",
        "axis_family": "4-axis",
        "applicability": "mg400_m1pro",
        "priority": "high",
        "safety_level": "caution",
        "source_type": "official_github",
        "code_related": True,
    },
    {
        "path": "02_api_sdk/official_mg400_code_tcp-ip-4axis-python_repo/main.py",
        "doc_type": "sdk_code",
        "doc_title": "main.py (TCP/IP demo entry)",
        "doc_version": "github",
        "publish_date": "unknown",
        "language": "en",
        "robot_model": "mg400",
        "axis_family": "4-axis",
        "applicability": "mg400_m1pro",
        "priority": "medium",
        "safety_level": "caution",
        "source_type": "official_github",
        "code_related": True,
    },
    {
        "path": "02_api_sdk/official_mg400_code_tcp-ip-4axis-python_repo/files/alarm_controller.json",
        "doc_type": "error_code",
        "doc_title": "alarm_controller.json",
        "doc_version": "github",
        "publish_date": "unknown",
        "language": "en",
        "robot_model": "mg400",
        "axis_family": "4-axis",
        "applicability": "mg400_m1pro",
        "priority": "high",
        "safety_level": "warning",
        "source_type": "official_github",
    },
    {
        "path": "02_api_sdk/official_mg400_code_tcp-ip-4axis-python_repo/files/alarm_servo.json",
        "doc_type": "error_code",
        "doc_title": "alarm_servo.json",
        "doc_version": "github",
        "publish_date": "unknown",
        "language": "en",
        "robot_model": "mg400",
        "axis_family": "4-axis",
        "applicability": "mg400_m1pro",
        "priority": "high",
        "safety_level": "warning",
        "source_type": "official_github",
    },
    # --- C++ SDK (headers + core impl only via globs below if listed) ---
    {
        "path": "02_api_sdk/official_mg400_code_tcp-ip-4axis-cpp_repo/README-EN.md",
        "doc_type": "sdk_code",
        "doc_title": "TCP-IP-4Axis-CPP README (EN)",
        "doc_version": "github",
        "publish_date": "unknown",
        "language": "en",
        "robot_model": "mg400",
        "axis_family": "4-axis",
        "applicability": "mg400_m1pro",
        "priority": "medium",
        "safety_level": "caution",
        "source_type": "official_github",
        "code_related": True,
    },
    # --- C# SDK ---
    {
        "path": "02_api_sdk/official_mg400_code_tcp-ip-4axis-csharp_repo/README-EN.md",
        "doc_type": "sdk_code",
        "doc_title": "TCP-IP-4Axis-CSharp README (EN)",
        "doc_version": "github",
        "publish_date": "unknown",
        "language": "en",
        "robot_model": "mg400",
        "axis_family": "4-axis",
        "applicability": "mg400_m1pro",
        "priority": "medium",
        "safety_level": "caution",
        "source_type": "official_github",
        "code_related": True,
    },
    # --- ROS ---
    {
        "path": "02_api_sdk/official_mg400_code_mg400-ros_repo/README-EN.md",
        "doc_type": "sdk_code",
        "doc_title": "MG400 ROS README (EN)",
        "doc_version": "github",
        "publish_date": "unknown",
        "language": "en",
        "robot_model": "mg400",
        "axis_family": "4-axis",
        "applicability": "direct_mg400",
        "priority": "medium",
        "safety_level": "caution",
        "source_type": "official_github",
        "code_related": True,
    },
    # --- Demo training PDFs (top-level official guides) ---
    {
        "path": "03_demo_training/official_mg400_demo_palletizing-guide_2023-06-16_en.pdf",
        "doc_type": "demo_guide",
        "doc_title": "MG400 Demo: Palletizing Guide",
        "doc_version": "2023-06-16",
        "publish_date": "2023-06-16",
        "language": "en",
        "robot_model": "mg400",
        "axis_family": "4-axis",
        "applicability": "direct_mg400",
        "priority": "high",
        "safety_level": "caution",
        "source_type": "official_demo",
    },
    {
        "path": "03_demo_training/official_mg400_demo_dynamic-palletizing-guide_2023-06-16_en.pdf",
        "doc_type": "demo_guide",
        "doc_title": "MG400 Demo: Dynamic Palletizing Guide",
        "doc_version": "2023-06-16",
        "publish_date": "2023-06-16",
        "language": "en",
        "robot_model": "mg400",
        "axis_family": "4-axis",
        "applicability": "direct_mg400",
        "priority": "high",
        "safety_level": "caution",
        "source_type": "official_demo",
    },
    {
        "path": "03_demo_training/official_mg400_demo_vision-palletizing-guide_2023-06-16_en.pdf",
        "doc_type": "demo_guide",
        "doc_title": "MG400 Demo: Vision Palletizing Guide",
        "doc_version": "2023-06-16",
        "publish_date": "2023-06-16",
        "language": "en",
        "robot_model": "mg400",
        "axis_family": "4-axis",
        "applicability": "direct_mg400",
        "priority": "high",
        "safety_level": "caution",
        "source_type": "official_demo",
    },
    {
        "path": "03_demo_training/official_mg400_demo_standard-conveyor-guide_2023-06-16_en.pdf",
        "doc_type": "demo_guide",
        "doc_title": "MG400 Demo: Standard Conveyor Guide",
        "doc_version": "2023-06-16",
        "publish_date": "2023-06-16",
        "language": "en",
        "robot_model": "mg400",
        "axis_family": "4-axis",
        "applicability": "direct_mg400",
        "priority": "high",
        "safety_level": "caution",
        "source_type": "official_demo",
    },
    {
        "path": "03_demo_training/official_mg400_demo_mobile-phone-chip-sorting-guide_2023-06-16_en.pdf",
        "doc_type": "demo_guide",
        "doc_title": "MG400 Demo: Mobile Phone Chip Sorting Guide",
        "doc_version": "2023-06-16",
        "publish_date": "2023-06-16",
        "language": "en",
        "robot_model": "mg400",
        "axis_family": "4-axis",
        "applicability": "direct_mg400",
        "priority": "high",
        "safety_level": "caution",
        "source_type": "official_demo",
    },
    {
        "path": "03_demo_training/official_mg400_demo_training-system-installation-guide_2023-06-16_en.pdf",
        "doc_type": "demo_guide",
        "doc_title": "MG400 Training System Installation Guide",
        "doc_version": "2023-06-16",
        "publish_date": "2023-06-16",
        "language": "en",
        "robot_model": "mg400",
        "axis_family": "4-axis",
        "applicability": "direct_mg400",
        "priority": "high",
        "safety_level": "warning",
        "source_type": "official_demo",
    },
]

# Backward-compatible alias
P0_SOURCES = CORE_SOURCES

# Curated markdown under chatbot/data/curated
CURATED_SOURCES: list[dict] = [
    {
        "path": "curated:mg400_product_specs.md",
        "doc_type": "datasheet",
        "doc_title": "MG400 Product Spec Snapshot (curated from official product page)",
        "doc_version": "product-page",
        "publish_date": "unknown",
        "language": "en",
        "robot_model": "mg400",
        "axis_family": "4-axis",
        "applicability": "direct_mg400",
        "priority": "high",
        "safety_level": "caution",
        "source_type": "curated_official",
    },
    {
        "path": "curated:mg400_tcp_ports_and_connect.md",
        "doc_type": "cheat_sheet",
        "doc_title": "MG400 TCP Ports and Connection Cheat-sheet",
        "doc_version": "curated",
        "publish_date": "unknown",
        "language": "en",
        "robot_model": "mg400",
        "axis_family": "4-axis",
        "applicability": "mg400_m1pro",
        "priority": "high",
        "safety_level": "critical",
        "source_type": "curated_official",
        "code_related": True,
    },
    {
        "path": "curated:mg400_safety_before_motion.md",
        "doc_type": "cheat_sheet",
        "doc_title": "MG400 Safety Checklist Before Motion",
        "doc_version": "curated",
        "publish_date": "unknown",
        "language": "en",
        "robot_model": "mg400",
        "axis_family": "4-axis",
        "applicability": "direct_mg400",
        "priority": "high",
        "safety_level": "critical",
        "source_type": "curated_official",
    },
    {
        "path": "curated:mg400_python_tcp_skeleton.md",
        "doc_type": "cheat_sheet",
        "doc_title": "MG400 Python TCP Skeleton (connection-first)",
        "doc_version": "curated",
        "publish_date": "unknown",
        "language": "en",
        "robot_model": "mg400",
        "axis_family": "4-axis",
        "applicability": "mg400_m1pro",
        "priority": "high",
        "safety_level": "critical",
        "source_type": "curated_official",
        "code_related": True,
    },
]

FAQ_META = {
    "doc_type": "faq",
    "robot_model": "mg400",
    "axis_family": "4-axis",
    "applicability": "direct_mg400",
    "priority": "high",
    "safety_level": "caution",
    "source_type": "official_faq",
    "language": "en",
    "doc_version": "current",
    "publish_date": "unknown",
}

CASE_META = {
    "doc_type": "case_study",
    "robot_model": "mg400",
    "axis_family": "4-axis",
    "applicability": "direct_mg400",
    "priority": "medium",
    "safety_level": "normal",
    "source_type": "official_web",
    "language": "en",
    "doc_version": "current",
    "publish_date": "unknown",
}

# Glob expansions relative to CORPUS_RAW (deduped against CORE_SOURCES by path)
# Skip: CAD, build artifacts, Chinese TCP PDF, duplicate chapter PDFs already covered
# by top-level demo guides, nlohmann headers, alarm JSON duplicates in other repos.
GLOB_SOURCES: list[dict] = [
    # C++ API source (not build tree)
    {
        "glob": "02_api_sdk/official_mg400_code_tcp-ip-4axis-cpp_repo/CppDemo/api/*.{h,cpp}",
        "doc_type": "sdk_code",
        "priority": "medium",
        "safety_level": "caution",
        "source_type": "official_github",
        "code_related": True,
        "applicability": "mg400_m1pro",
        "robot_model": "mg400",
        "axis_family": "4-axis",
        "language": "en",
        "doc_version": "github",
        "publish_date": "unknown",
    },
    {
        "glob": "02_api_sdk/official_mg400_code_tcp-ip-4axis-cpp_repo/CppDemo/*.{cpp,h}",
        "doc_type": "sdk_code",
        "priority": "low",
        "safety_level": "caution",
        "source_type": "official_github",
        "code_related": True,
        "applicability": "mg400_m1pro",
        "robot_model": "mg400",
        "axis_family": "4-axis",
        "language": "en",
        "doc_version": "github",
        "publish_date": "unknown",
    },
    # C# API
    {
        "glob": "02_api_sdk/official_mg400_code_tcp-ip-4axis-csharp_repo/CSharpTcpDemo/com.dobot.api/*.cs",
        "doc_type": "sdk_code",
        "priority": "medium",
        "safety_level": "caution",
        "source_type": "official_github",
        "code_related": True,
        "applicability": "mg400_m1pro",
        "robot_model": "mg400",
        "axis_family": "4-axis",
        "language": "en",
        "doc_version": "github",
        "publish_date": "unknown",
    },
    # ROS: README already in core; add srv + key sources, skip nlohmann / duplicate alarms
    {
        "glob": "02_api_sdk/official_mg400_code_mg400-ros_repo/bringup/srv/*.srv",
        "doc_type": "ros_api",
        "priority": "medium",
        "safety_level": "caution",
        "source_type": "official_github",
        "code_related": True,
        "applicability": "direct_mg400",
        "robot_model": "mg400",
        "axis_family": "4-axis",
        "language": "en",
        "doc_version": "github",
        "publish_date": "unknown",
    },
    {
        "glob": "02_api_sdk/official_mg400_code_mg400-ros_repo/bringup/msg/*.msg",
        "doc_type": "ros_api",
        "priority": "low",
        "safety_level": "normal",
        "source_type": "official_github",
        "code_related": True,
        "applicability": "direct_mg400",
        "robot_model": "mg400",
        "axis_family": "4-axis",
        "language": "en",
        "doc_version": "github",
        "publish_date": "unknown",
    },
    {
        "glob": "02_api_sdk/official_mg400_code_mg400-ros_repo/bringup/src/*.cpp",
        "doc_type": "sdk_code",
        "priority": "low",
        "safety_level": "caution",
        "source_type": "official_github",
        "code_related": True,
        "applicability": "direct_mg400",
        "robot_model": "mg400",
        "axis_family": "4-axis",
        "language": "en",
        "doc_version": "github",
        "publish_date": "unknown",
    },
    {
        "glob": "02_api_sdk/official_mg400_code_mg400-ros_repo/bringup/include/bringup/*.h",
        "doc_type": "sdk_code",
        "priority": "low",
        "safety_level": "caution",
        "source_type": "official_github",
        "code_related": True,
        "applicability": "direct_mg400",
        "robot_model": "mg400",
        "axis_family": "4-axis",
        "language": "en",
        "doc_version": "github",
        "publish_date": "unknown",
    },
    {
        "glob": "02_api_sdk/official_mg400_code_mg400-ros_repo/rosdemo/src/*.cpp",
        "doc_type": "sdk_code",
        "priority": "low",
        "safety_level": "caution",
        "source_type": "official_github",
        "code_related": True,
        "applicability": "direct_mg400",
        "robot_model": "mg400",
        "axis_family": "4-axis",
        "language": "en",
        "doc_version": "github",
        "publish_date": "unknown",
    },
    # Training system: chapter PDFs + lua scripts (skip project JSON config noise)
    {
        "glob": "03_demo_training/official_mg400_demo_training-system-user-guide_2023-02-06_en_extracted/**/*.pdf",
        "doc_type": "demo_guide",
        "priority": "medium",
        "safety_level": "caution",
        "source_type": "official_demo",
        "applicability": "direct_mg400",
        "robot_model": "mg400",
        "axis_family": "4-axis",
        "language": "en",
        "doc_version": "2023-02-06",
        "publish_date": "2023-02-06",
    },
    {
        "glob": "03_demo_training/official_mg400_demo_training-system-user-guide_2023-02-06_en_extracted/**/*.lua",
        "doc_type": "demo_script",
        "priority": "medium",
        "safety_level": "caution",
        "source_type": "official_demo",
        "code_related": True,
        "applicability": "direct_mg400",
        "robot_model": "mg400",
        "axis_family": "4-axis",
        "language": "en",
        "doc_version": "2023-02-06",
        "publish_date": "2023-02-06",
    },
]

# Path fragments to skip always
SKIP_PATH_PARTS = (
    "/nlohmann/",
    "\\nlohmann\\",
    "/__pycache__/",
    "\\__pycache__\\",
    "/build-",
    "\\build-",
    "/bin/",
    "\\bin\\",
    "/Debug/",
    "\\Debug\\",
    "/Release/",
    "\\Release\\",
    ".stp",
    ".STL",
    ".stl",
    ".zip",
    ".sol",
    # Chinese TCP guide (duplicate of EN)
    "TCP_IP远程控制",
    # Duplicate alarms already ingested from Python repo
    "mg400-ros_repo/bringup/alarmFile/",
    "mg400-ros_repo\\bringup\\alarmFile\\",
    "rosdemo/alarmFile/",
    "rosdemo\\alarmFile\\",
    "tcp-ip-4axis-cpp_repo/CppDemo/alarm_",
    "tcp-ip-4axis-csharp_repo/alarm_",
    "tcp-ip-4axis-csharp_repo\\alarm_",
    # Designer / generated UI noise
    "MainForm.Designer.cs",
    "Properties/",
    "Properties\\",
    "Form.ui",
    "main_window.ui",
    "moc_",
    "ui_Form.h",
    "object_script.",
    "Makefile",
    "CMakeLists.txt",
    "package.xml",
    ".pro.user",
    "Newtonsoft.Json",
    "App.config",
    # Vision binary projects
    "Vision Program Demo",
)

# FAQ / case HTML globs
FAQ_GLOB = "04_faq_pages/*.html"
CASE_GLOB = "05_case_application_pages/*.html"

# ---------------------------------------------------------------------------
# Tight corpus policy (default for production chatbot)
# Keep high-signal manuals/API/Python/demos/curated/FAQ(scrubbed).
# Drop marketing pages, multi-language SDKs, ROS micro-files, alarms (noise),
# duplicate training chapters, and known-empty/broken PDFs.
# ---------------------------------------------------------------------------
TIGHT_EXCLUDE_PATH_SUBSTRINGS = (
    # Alarms dominate index and pollute non-error questions
    "alarm_controller.json",
    "alarm_servo.json",
    # Scanned / empty / broken PDFs
    "parameter-document_2022-07-28",
    "official_mg400_demo_palletizing-guide_2023-06-16_en.pdf",  # corrupt stream
    # Chinese TCP guide (duplicate of EN)
    "TCP_IP远程控制",
)

# In tight mode, only these glob families are allowed (usually none)
TIGHT_GLOB_ALLOW_SUBSTRINGS = (
    # Chapter 2 palletizing replaces corrupt top-level palletizing PDF
    "training-system-user-guide_2023-02-06_en_extracted/Chapter2/",
    # Optional Lua for demo code answers (small, high signal)
    "training-system-user-guide_2023-02-06_en_extracted/",
)

TIGHT_GLOB_ALLOW_SUFFIXES = (".lua", ".pdf")

# Core paths always kept in tight (subset of CORE_SOURCES filtered at runtime)
TIGHT_DOC_TYPES_DROP = frozenset(
    {
        "case_study",
        "error_code",  # load via --full when debugging alarms
        "ros_api",
    }
)

# Path substrings for multi-SDK noise dropped in tight (kept in --full)
TIGHT_DROP_PATH_SUBSTRINGS = (
    "tcp-ip-4axis-cpp_repo",
    "tcp-ip-4axis-csharp_repo",
    "mg400-ros_repo",
    "05_case_application_pages",
    # Duplicate chapter PDFs (top-level demo guides already cover topics);
    # Chapter2 PDF is re-added via tight globs only.
    "training-system-user-guide_2023-02-06_en_extracted/Chapter1/",
    "training-system-user-guide_2023-02-06_en_extracted/Chapter3/",
    "training-system-user-guide_2023-02-06_en_extracted/Chapter4/",
    "training-system-user-guide_2023-02-06_en_extracted/Chapter5/",
    "training-system-user-guide_2023-02-06_en_extracted/Chapter6/",
)

# HTML footer/nav noise patterns stripped from FAQ/case extracts
HTML_NOISE_LINE_PATTERNS = (
    r"^Products$",
    r"^Industries$",
    r"^Applications$",
    r"^Insights$",
    r"^Investor Relations$",
    r"^Support$",
    r"^About Dobot$",
    r"^Search$",
    r"^User$",
    r"^Home$",
    r"^Contact$",
    r"^English$",
    r"^Deutsch$",
    r"^Español$",
    r"^Français$",
    r"^Italian$",
    r"^Polski$",
    r"^Nederlands$",
    r"^Portuguese$",
    r"^Pусский$",
    r"^日本語$",
    r"^Thai$",
    r"^Indonesia$",
    r"^한국어$",
    r"^繁体中文$",
    r"^简体中文$",
    r"^Quick Links$",
    r"^Follow Us$",
    r"^Subscribe to the latest updates\.?$",
    r"^Did it solve your problem\?$",
    r"^Yes$",
    r"^No$",
    r"^Customer Service$",
    r"^Customer Service Email$",
    r"^sales@dobot-robots\.com$",
    r"^support@dobot-robots\.com$",
    r"^new$",
    r"^Learn More$",
    r"^Back$",
    r"^Questions$",
    r"^Contact Us$",
)
