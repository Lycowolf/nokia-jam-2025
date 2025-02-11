#![allow(clippy::type_complexity)]

use bevy::math::bounding::{Aabb2d, BoundingVolume, IntersectsVolume};
use bevy:: prelude::*;
use seldom_pixel::prelude::*;

const SCREEN_W: f32 = 84.0;
const SCREEN_H: f32 = 48.0;
const PIXEL_SCALE: i32 = 8;
const INIT_BALL_POS: Vec2 = Vec2{x: 16.0, y: 22.0};
const INIT_BALL_VELOCITY: Vec2 = Vec2{x: 20.0, y: 25.0};
const BALL_HALF_SIZE: Vec2 = Vec2{x: 2.0, y: 2.0};

const PADDLE_HALF_SIZE_H: Vec2 = Vec2{x: 6.5, y: 0.5};
const PADDLE_HALF_SIZE_V: Vec2 = Vec2{x: 0.5, y: 6.5};
const PADDLE_SPEED: f32 = 60.0;

// TODO: migrate to leafwing-input-manager or something
const K_LEFT: [KeyCode; 3] = [KeyCode::ArrowLeft, KeyCode::KeyA, KeyCode::Numpad4];
const K_RIGHT: [KeyCode; 3] = [KeyCode::ArrowRight, KeyCode::KeyD, KeyCode::Numpad6];
const K_UP: [KeyCode; 3] = [KeyCode::ArrowUp, KeyCode::KeyW, KeyCode::Numpad8];
const K_DOWN: [KeyCode; 3] = [KeyCode::ArrowDown, KeyCode::KeyS, KeyCode::Numpad2];

#[derive(Component, Debug)]
struct Collider(Aabb2d);
impl Default for Collider {
    fn default() -> Self {
        unimplemented!("Collider doesn't have a meaningful default")
    }
}

#[derive(Component, Debug)]
#[require(PxPosition, PxSubPosition, PxVelocity)]
struct Ball{}

#[derive(Component, Debug)]
struct Horizontal{}

#[derive(Component, Debug)]
struct Vertical{}

#[derive(Component, Debug)]
#[require(PxSprite, PxSubPosition, Collider)] // also Horizontal or Vertical
struct Paddle{}

#[derive(Component, Debug)]
#[require(PxPosition, Collider)]
struct BorderSegment{}

#[derive(Component, Debug)]
struct Score(u32);

fn bounce_ball(
    mut score: Single<&mut Score>,
    mut balls: Query<(&mut PxSubPosition, &mut PxVelocity), With<Ball>>, 
    mut other_colliders: Query<(&Collider, Has<Paddle>), Without<Ball>>,
) {
    for (mut ball_center, mut velocity) in &mut balls {
        let ball_collider  = Aabb2d::new(ball_center.0, BALL_HALF_SIZE);
        for (other_collider, is_paddle) in &mut other_colliders {
            // FIXME: we sometimes doublecount collisions. IDK why
            if ball_collider.intersects(&other_collider.0) {
                if is_paddle {
                    score.0 += 1;
                } 
                let closest = other_collider.0.closest_point(ball_center.0);
                let offset = closest - ball_collider.center();
                // bounce only if the velocity is oposite of direction we came from to prevent ball getting stuck in paddles / walls
                if offset.x.abs() > offset.y.abs() { // collision in X axis
                    if offset.x.signum() == velocity.0.x.signum() {
                        velocity.0.x = -velocity.0.x;
                    }
                } else if offset.y.signum() == velocity.0.y.signum() {
                        velocity.0.y = -velocity.0.y;
                }
            }
        }
    }
}

fn process_input(
    input: Res<ButtonInput<KeyCode>>,
    time: Res<Time>,
    mut horizontal: Query<&mut PxSubPosition, (With<Paddle>, With<Horizontal>, Without<Vertical>)>, // tell bevy ECS these are disjoint
    mut vertical: Query<&mut PxSubPosition, (With<Paddle>, With<Vertical>, Without<Horizontal>)>
) {
    let epsilon = 0.01;

    let mut velocity = 0.0;
    if input.any_pressed(K_LEFT) { velocity = -PADDLE_SPEED}
    if input.any_pressed(K_RIGHT) { velocity = PADDLE_SPEED}
    velocity *= time.delta_secs();
    for mut paddle_pos in &mut horizontal {
        paddle_pos.x = (paddle_pos.x + velocity).clamp(PADDLE_HALF_SIZE_H.x - epsilon, SCREEN_W - PADDLE_HALF_SIZE_H.x - 1.0 + epsilon)
    }
    
    let mut velocity = 0.0;
    if input.any_pressed(K_UP) { velocity = PADDLE_SPEED}
    if input.any_pressed(K_DOWN) { velocity = -PADDLE_SPEED}
    velocity *= time.delta_secs();
    for mut paddle_pos in &mut vertical {
            paddle_pos.y = (paddle_pos.y + velocity).clamp(PADDLE_HALF_SIZE_V.y - epsilon, SCREEN_H - PADDLE_HALF_SIZE_V.y - 1.0 + epsilon)
    }
}

fn sync_paddle_colliders(mut paddles: Query<(&PxSubPosition, &mut Collider), With<Paddle>>) {
    for (position, mut collider) in &mut paddles {
        let mov = position.0 - collider.0.center();
        collider.0.translate_by(mov);
    }
}

fn display_score(scoreboard: Single<(&Score, &mut PxText)>) {
    let (score, mut text) = scoreboard.into_inner();
    text.into_inner().value = score.0.to_string();
}

fn init(mut time: ResMut<Time<Fixed>>, assets: Res<AssetServer>, mut commands: Commands) {
    //time.set_timestep_hz(405.0);

    commands.spawn(Camera2d);

    // scoreboard
    let text_font = TextFont {
        font_size: 8.0,
        ..default()
    };

    commands.spawn((
        Score(0),
        PxText {
            value: "0".to_string(),
            typeface: assets.load("typeface.png"),
        },
        PxRect(IRect::new(0, SCREEN_H as i32 / 2 - 4, SCREEN_W as i32,  SCREEN_H as i32 / 2 + 4))
    ));

    // borders
    commands.spawn(( // bottom
        Collider(Aabb2d{min: (0.0, -SCREEN_H).into(), max: (SCREEN_W, 0.0).into()}),
    ));
    commands.spawn(( // top
        Collider(Aabb2d{min: (0.0, SCREEN_H).into(), max: (SCREEN_W, SCREEN_H * 2.0).into()}),
    ));
    commands.spawn(( // left
        Collider(Aabb2d{min: (-SCREEN_W, 0.0).into(), max: (0.0, SCREEN_H).into()}),
    ));
    commands.spawn(( // right
        Collider(Aabb2d{min: (SCREEN_W, 0.0).into(), max: (SCREEN_W * 2.0, SCREEN_H).into()}),
    ));

    // ball
    commands.spawn((
        Ball{},
        PxSubPosition(INIT_BALL_POS),
        PxVelocity(INIT_BALL_VELOCITY),
        PxSprite(assets.load("ball.png")),
        Collider(Aabb2d::new(INIT_BALL_POS, BALL_HALF_SIZE)),
    ));

    // paddles
    // TODO: simplify using macro
    // collider center doesn't matter: it gets synced immediately to the PxSubPosition
    commands.spawn(( //bottom
        Paddle{},
        Horizontal{},
        PxSprite(assets.load("paddle_h.png")),
        PxSubPosition(Vec2{x: SCREEN_W / 2.0, y: 0.0}),
        Collider(Aabb2d::new(Vec2::default(), PADDLE_HALF_SIZE_H)),
    ));
    commands.spawn(( //top
        Paddle{},
        Horizontal{},
        PxSprite(assets.load("paddle_h.png")),
        PxSubPosition(Vec2{x: SCREEN_W / 2.0, y: SCREEN_H - 1.0}),
        Collider(Aabb2d::new(Vec2::default(), PADDLE_HALF_SIZE_H)),
    ));
    commands.spawn(( //left
        Paddle{},
        Vertical{},
        PxSprite(assets.load("paddle_v.png")),
        PxSubPosition(Vec2{x: 0.0, y: SCREEN_H / 2.0}),
        Collider(Aabb2d::new(Vec2::default(), PADDLE_HALF_SIZE_V)),
    ));
    commands.spawn(( //right
        Paddle{},
        Vertical{},
        PxSprite(assets.load("paddle_v.png")),
        PxSubPosition(Vec2{x: SCREEN_W - 1.0, y: SCREEN_H / 2.0}),
        Collider(Aabb2d::new(Vec2::default(), PADDLE_HALF_SIZE_V)),
    ));
}

fn main() {
    App::new()
    .add_plugins((
        DefaultPlugins.set(WindowPlugin {
            primary_window: Some(Window {
                resolution: (Vec2::new(SCREEN_W, SCREEN_H) * PIXEL_SCALE as f32).into(),
                title: "bevy-test".to_string(),
                ..default()
            }),
            ..default()
        }),
        PxPlugin::<Layer>::new(UVec2::new(SCREEN_W as u32, SCREEN_H as u32), "palette_1.png"),
    ))
    .insert_resource(ClearColor(Color::BLACK))
    .add_systems(Startup, init)
    .add_systems(Update, (process_input, display_score))
    .add_systems(FixedUpdate, (sync_paddle_colliders, bounce_ball).chain())
    .run();
}

#[px_layer]
struct Layer; // we use only single graphics layer