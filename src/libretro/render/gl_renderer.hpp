/*
    Copyright 2024 Jesse Talavera-Greenberg

    melonDS DS is free software: you can redistribute it and/or modify it under
    the terms of the GNU General Public License as published by the Free
    Software Foundation, either version 3 of the License, or (at your option)
    any later version.

    melonDS DS is distributed in the hope that it will be useful, but WITHOUT ANY
    WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
    FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with melonDS DS. If not, see http://www.gnu.org/licenses/.
*/

#ifndef MELONDSDS_RENDER_GL_RENDERER_HPP
#define MELONDSDS_RENDER_GL_RENDERER_HPP

#if defined(HAVE_OPENGL) || defined(HAVE_OPENGLES)

#include <memory>

#include <GPU_OpenGL.h>
#include <GPU_Hybrid.h>
#include <NDS.h>

namespace MelonDsDs {
    /// Whether melonDS is rendering through the frontend's OpenGL context: its GLRenderer, or
    /// (游典, MELONDSDS_HYBRID_GL) its HybridRenderer — the 3D on the GPU, the 2D by the software
    /// renderer, melonDS's own: the OpenGL 2D renderer garbles some games' 2D (二之国's opening;
    /// upstream melonDS #2768's kind).
    inline bool IsGlRenderer(const melonDS::Renderer& renderer) noexcept {
        return dynamic_cast<const melonDS::GLRenderer*>(&renderer) != nullptr
            || dynamic_cast<const melonDS::HybridRenderer*>(&renderer) != nullptr;
    }

    /// The renderer for the OpenGL render modes: the compute one as melonDS has it; the classic
    /// one melonDS's GLRenderer, or the HybridRenderer where MELONDSDS_HYBRID_GL says so.
    inline std::unique_ptr<melonDS::Renderer> MakeGlRenderer(melonDS::NDS& nds, bool compute) {
#ifdef MELONDSDS_HYBRID_GL
        if (!compute)
            return std::make_unique<melonDS::HybridRenderer>(nds);
#endif
        return std::make_unique<melonDS::GLRenderer>(nds, compute);
    }
}

#endif

#endif //MELONDSDS_RENDER_GL_RENDERER_HPP
