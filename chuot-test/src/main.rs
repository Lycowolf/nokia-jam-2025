use chuot::*;
use glam::Vec2;

/// Define a game state.
struct State {
    ball_position: Vec2,
    ball_velocity: Vec2,
    paddle_position: Vec2,
    score: u32,
    paused: bool,
}

// Chuot coordinate system is: (0,0) in the center, Y+ points down
const PADDLE_THICKNESS: f32 = 1.0;
const PADDLE_HALF_SIZE: f32 = 6.5;
const BALL_HALF_SIZE: f32 = 2.0;
const SCREEN_HALF_W: f32 = 84.0 / 2.0;
const SCREEN_HALF_H: f32 = 48.0 / 2.0;
const PADDLE_SPEED: Vec2 = Vec2::new(50.0, 50.0); // pixels per second
const BALL_VELOCITY: Vec2 = Vec2::new(35.0, 35.0);
const KEY_MAP: [(Vec2, [KeyCode; 3]); 4] = [
    (Vec2::new(0.0, -1.0), [KeyCode::ArrowUp, KeyCode::Numpad8, KeyCode::KeyW]),
    (Vec2::new(0.0, 1.0), [KeyCode::ArrowDown, KeyCode::Numpad2, KeyCode::KeyS]),
    (Vec2::new(1.0, 0.0), [KeyCode::ArrowRight, KeyCode::Numpad6, KeyCode::KeyD]),
    (Vec2::new(-1.0, 0.0), [KeyCode::ArrowLeft, KeyCode::Numpad4, KeyCode::KeyA]),
];

impl Game for State {
    /// Update the game, handle input, move enemies, etc.
    fn update(&mut self, ctx: Context) {
        // pause
        if ctx.key_pressed(KeyCode::Space) {self.paused = !self.paused}
        if self.paused {return}

        let elapsed = ctx.delta_time();

        // paddles
        let mut paddle_movement_mask = Vec2::ZERO;
        for (direction, keys) in KEY_MAP{
            for key in keys {
                if ctx.key_held(key) {paddle_movement_mask += direction};
            }
        }
        paddle_movement_mask = paddle_movement_mask.try_normalize().unwrap_or(Vec2::ZERO);
        self.paddle_position += paddle_movement_mask * PADDLE_SPEED * elapsed;
        let paddle_play_area = (
            Vec2::new(-SCREEN_HALF_W + PADDLE_HALF_SIZE, -SCREEN_HALF_H + PADDLE_HALF_SIZE), 
            Vec2::new(SCREEN_HALF_W - PADDLE_HALF_SIZE, SCREEN_HALF_H - PADDLE_HALF_SIZE)
        );
        self.paddle_position = self.paddle_position.clamp(paddle_play_area.0, paddle_play_area.1);

        //ball
        let ball_play_area = (
            Vec2::new(-SCREEN_HALF_W + BALL_HALF_SIZE, -SCREEN_HALF_H + BALL_HALF_SIZE), 
            Vec2::new(SCREEN_HALF_W - BALL_HALF_SIZE, SCREEN_HALF_H - BALL_HALF_SIZE)
        );
        self.ball_position += self.ball_velocity * elapsed;
        let clamped_position = self.ball_position.clamp(ball_play_area.0, ball_play_area.1);
        // detect collisions
        if self.ball_position.x < ball_play_area.0.x || self.ball_position.x > ball_play_area.1.x {
            // collision in X
            if self.ball_position.y > self.paddle_position.y - PADDLE_HALF_SIZE  
            && self.ball_position.y < self.paddle_position.y + PADDLE_HALF_SIZE {
                self.score += 1;
            }
            // TODO: compute the bounce accurately
            self.ball_position = clamped_position;
            self.ball_velocity *= Vec2::new(-1.0, 1.0);
        }
        if self.ball_position.y < ball_play_area.0.y || self.ball_position.y > ball_play_area.1.y {
            // collision in Y
            if self.ball_position.x > self.paddle_position.x - PADDLE_HALF_SIZE  
            && self.ball_position.x < self.paddle_position.x + PADDLE_HALF_SIZE {
                self.score += 1;
            }
            // TODO: compute the bounce accurately
            self.ball_position = clamped_position;
            self.ball_velocity *= Vec2::new(1.0, -1.0);
        }

    }

    /// Render the game.
    fn render(&mut self, ctx: Context) {
        // scoreboard
        ctx.text("font", &self.score.to_string())
        .use_main_camera()
        .draw();

        // ball
        ctx.sprite("ball")
        .pivot_center() // also changes where the sprite is rendered
        .translate(self.ball_position)
        .draw();
        
        // paddles
        let paddles: [(f32, f32, _); 4] = [
            (self.paddle_position.x, - SCREEN_HALF_H + PADDLE_THICKNESS / 2.0, true),
            (self.paddle_position.x, SCREEN_HALF_H - PADDLE_THICKNESS / 2.0, true),
            (-SCREEN_HALF_W + PADDLE_THICKNESS / 2.0, self.paddle_position.y, false),
            (SCREEN_HALF_W - PADDLE_THICKNESS / 2.0, self.paddle_position.y, false),
        ];
        for (x, y, horizontal) in paddles {
            ctx.sprite(if horizontal {"paddle_h"} else {"paddle_v"})
            .pivot_center()
            .translate((x, y))
            .draw();
        }
    }
}

fn main() {
  let game = State{
        ball_position: Vec2::new(0.0, 0.0),
        ball_velocity: BALL_VELOCITY,
        paddle_position: Vec2::new(0.0, 0.0),
        score: 0,
        paused: false
    };

  let engine_config = Config{
    buffer_width: SCREEN_HALF_W * 2.0,
    buffer_height: SCREEN_HALF_H * 2.0,
    scaling: 8.0, 
    background_color: RGBA8::new(0, 0, 0, 255), 
    title: "Chuot test".to_string(),
    update_delta_time: 1.0 / 60.0,
    vsync: true,
    ..Default::default()};
    game.run(chuot::load_assets!(), engine_config);
}