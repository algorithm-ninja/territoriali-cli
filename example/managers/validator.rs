use std::env;
use std::io::stdin;

fn main()
{
    let args: Vec<_> = env::args().skip(1).collect();
    assert_eq!(args.len(), 1);
    let mut input = String::new();
    stdin().read_line(&mut input).unwrap();
    let n = match input.trim().parse::<u64>()
    {
        Ok(x) => x,
        Err(why) => panic!("{}: {}", why, input),
    };
    for _ in 0..n
    {
        input = String::new();
        stdin().read_line(&mut input).unwrap();
        let v: Vec<_> = input
            .trim()
            .split(" ")
            .map(|x| x.parse::<u64>().unwrap())
            .collect();
        assert_eq!(v.len(), 2);
    }
}
