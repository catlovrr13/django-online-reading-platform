// components
// import GridMotion from "@/components/GridMotion";
import { Button } from "@/components/ui/button";
import ScrollFloat from "@/components/ScrollFloat";
import {
  Carousel,
  CarouselContent,
  CarouselItem,
  CarouselNext,
  CarouselPrevious,
} from "@/components/ui/carousel";
import { Card, CardContent } from "@/components/ui/card";
import { Header1, Header2, Header3 } from "@/components/custom-components/headers";

// media
import dDark from "@/assets/media/hero-d-dark.svg"
import dLight from "@/assets/media/hero-d-light.svg"
import mDark from "@/assets/media/hero-m-dark.svg"
import mLight from "@/assets/media/hero-m-light.svg"

// function
import { useTheme } from "@/components/theme-provider";

export const iframeHeight = "800px";

export default function Page() {
  const { theme } = useTheme();
  const heroBG =
    theme === "dark" ? `bg-stone-900 opacity-40` : `bg-stone-200 opacity-40`;
  const cardAd =
    theme === "dark" ? `bg-stone-100 opacity-10` : `bg-stone-900 opacity-20`;
    const heroImage = theme === 'dark' ? dDark : dLight;

  return (
    <>
      <div className="flex flex-col gap-0 justify-center">
        {/* hero section */}
          <div className="relative flex overflow-hidden rounded-b-[100px] mb-10 drop-shadow-lg dark:drop-shadow-stone-900 dark:drop-shadow-xl">
            <div className="absolute z-10 flex flex-col md:flex-row p-10">
              <div>
                <Header1 text={"theonyxpub."} cl={'text-3xl md:text-5xl'}/>
                <Header3 text={"hevccjsgdv"} />
              </div>
              <div>

              </div>
            </div>
            <img
              src={heroImage}
              alt="hero"
              className="w-full h-[90%] object-cover rounded-b-[100px] scale-[1.01]"
            />
          </div>


        {/* genre */}
        <div
          className={`overflow-hidden w-full max-w-2xl flex flex-col gap-5 p-5 justify-center items-center`}
        >
          <ScrollFloat
            animationDuration={3}
            ease="back.inOut(2)"
            scrollStart="center bottom+=50%"
            scrollEnd="bottom bottom-=40%"
            stagger={0.04}
          >
            Genres
          </ScrollFloat>
          <Carousel
            opts={{
              align: "start",
            }}
            className="w-full max-w-[12rem] sm:max-w-xs md:max-w-sm"
          >
            <CarouselContent>
              {Array.from({ length: 5 }).map((_, index) => (
                <CarouselItem key={index} className="basis-1/2 lg:basis-1/3">
                  <div className="p-1">
                    <Card>
                      <CardContent className="flex aspect-square items-center justify-center p-6">
                        <span className="text-3xl font-semibold">
                          {index + 1}
                        </span>
                      </CardContent>
                    </Card>
                  </div>
                </CarouselItem>
              ))}
            </CarouselContent>
            <CarouselPrevious />
            <CarouselNext />
          </Carousel>
        </div>

        {/* subscription ad */}
        <div className={`h-100 ${heroBG} flex flex-col p-10 justify-center`}>
          <div className={`h-50 w-full max-w-3xl mx-auto ${cardAd}`}></div>
        </div>
      </div>
    </>
  );
}
