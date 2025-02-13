use macroquad::prelude::*;

#[derive(Debug, Default)]
struct State {
}

fn window_conf() -> Conf {
    Conf {
        window_title: "Macroquad test".to_string(),
        window_width: 84,
        window_height: 48,
        high_dpi: false,
        fullscreen: false,
        sample_count: 1,
        window_resizable: true,
        ..Default::default()
    }
}

#[macroquad::main(window_conf)]
async fn main() {
    let (screen_w, screen_h) = (window_conf().window_width as f32, window_conf().window_height as f32);

    // Fixed resolution pixellated game: render to a texture, then project that texture to the screen at the end of game loop
    // Macroquad's default coordinate system: (0, 0) is top-left, +Y points down.
    let render_target = render_target(84, 48);
    render_target.texture.set_filter(FilterMode::Nearest);
    let low_res_camera = Camera2D {
        zoom: vec2(1.0 / screen_w * 2.0, 1.0 / screen_h * 2.0), // I am not completely sure why and how is this necessary
        target: vec2(0.0, 0.0),
        offset: vec2(-1.0, -1.0),
        render_target: Some(render_target.clone()),
        ..Default::default()
    };

    // 

    // Window settings
    request_new_screen_size(window_conf().window_width as f32 * 8.0, window_conf().window_height as f32 * 8.0);

    // load assets
    let mut font = load_ttf_font_from_bytes(include_bytes!("../Tiny5/Tiny5-LCDBold.ttf")).unwrap();
    font.set_filter(FilterMode::Nearest);
    //font.populate_font_cache(characters, size);

    // initial game state
    let mut state = State::default();

    let mut font_size = 8;

    loop {
        // render to "pixel space"
        set_camera(&low_res_camera);

        clear_background(BLACK);

        if is_key_pressed(KeyCode::Up) {font_size += 1}
        if is_key_pressed(KeyCode::Down) {font_size -= 1}

        draw_text_ex("Hello, Macroquad!", 0.0, 8.0, TextParams{font: Some(&font), font_size, font_scale: 0.125, ..Default::default()});

        // render to screen space
        set_default_camera();
        clear_background(BLACK);
        draw_texture_ex(
            &render_target.texture,
            0.,
            0.,
            WHITE,
            DrawTextureParams {
                dest_size: Some(vec2(screen_width(), screen_height())),
                ..Default::default()
            },
        );
        next_frame().await
    }
}